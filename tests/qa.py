"""
KIBH Stage 2 QA pass.

Crawls every page, verifies every internal link resolves, captures console
errors, and checks for horizontal overflow / text clipping at each breakpoint.

    python tests/qa.py [base_url]
"""

import sys
import re
import pathlib
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4173").rstrip("/")
SHOTS = pathlib.Path(__file__).parent / "screenshots"

PAGES = [
    "/",
    "/e-rechnung/",
    "/deep-reading-engine/",
    "/ergebnisse/",
    "/ergebnisse/potenzial-analyse/",
    "/ergebnisse/kommunikation/",
    "/ergebnisse/u2care/",
    "/ergebnisse/automatische-rechnungspruefung/",
    "/kontakt/",
    "/impressum/",
    "/vertraulichkeit/",
]

VIEWPORTS = {
    "mobile": (390, 844),
    # 768 is one pixel above the <=767px type scale, so it renders desktop-sized
    # text in a narrow column -- the worst case for German compounds.
    "tablet-sm": (768, 1024),
    "tablet": (900, 1200),
    # Just above the nav's drawer breakpoint. The old 900/1440 pair straddled
    # this band, so a header that overflowed only between them went unseen.
    "laptop": (1040, 900),
    "desktop": (1440, 1000),
}

problems = []
checked_links = {}


def check_link(page, url):
    """Resolve an internal link once, caching the status."""
    if url in checked_links:
        return checked_links[url]
    resp = page.request.get(url)
    checked_links[url] = resp.status
    return resp.status


def audit_overflow(page):
    """Report elements wider than the viewport, and clipped text boxes."""
    return page.evaluate(
        """() => {
        const vw = document.documentElement.clientWidth;
        const out = { docScroll: document.documentElement.scrollWidth > vw + 1,
                      wide: [], clipped: [], overflowing: [] };
        // Element-level horizontal overflow. Caught even when an ancestor has
        // overflow-x hidden, which is exactly the case a scrollWidth check on
        // the document alone would miss.
        for (const el of document.querySelectorAll('body *')) {
            if (el.classList.contains('visually-hidden')) continue;
            // decorative-only subtrees are allowed to be clipped
            if (el.getAttribute('aria-hidden') === 'true') continue;
            // An absolutely-positioned descendant (the nav dropdown) is meant to
            // extend past its parent; that inflates scrollWidth without being a
            // layout defect.
            if ([...el.querySelectorAll('*')].some(d => {
                const pos = getComputedStyle(d).position;
                return pos === 'absolute' || pos === 'fixed';
            })) continue;
            if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0) {
                out.overflowing.push(
                    el.tagName.toLowerCase() + '.' +
                    String(el.className).trim().split(/\\s+/).join('.') +
                    ' [' + el.scrollWidth + ' > ' + el.clientWidth + ']');
            }
        }
        out.overflowing = [...new Set(out.overflowing)].slice(0, 8);
        for (const el of document.querySelectorAll('body *')) {
            const r = el.getBoundingClientRect();
            if (r.width === 0 && r.height === 0) continue;
            if (r.right > vw + 1.5 || r.left < -1.5) {
                const s = el.className && typeof el.className === 'string'
                    ? '.' + el.className.trim().split(/\\s+/).join('.') : '';
                out.wide.push(el.tagName.toLowerCase() + s +
                    ' [' + Math.round(r.left) + '→' + Math.round(r.right) + ' vw=' + vw + ']');
            }
            // text overflowing its own box (a real clipping bug, not just scroll).
            // .visually-hidden is clipped by design — that is how screen-reader-
            // only text works — so it is not a defect.
            const cs = getComputedStyle(el);
            if (el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0 &&
                cs.overflowY === 'hidden' &&
                el.getAttribute('aria-hidden') !== 'true' &&
                !el.classList.contains('visually-hidden')) {
                out.clipped.push(el.tagName.toLowerCase() + '.' +
                    String(el.className).trim().split(/\\s+/).join('.'));
            }
        }
        out.wide = [...new Set(out.wide)].slice(0, 8);
        out.clipped = [...new Set(out.clipped)].slice(0, 8);
        return out;
    }"""
    )


def audit_wordfit(page):
    """Report text whose longest unbreakable unit is wider than its own box.

    overflow-wrap keeps such text inside the box, so the element-level overflow
    check above stays silent -- but the browser has to chop the word with no
    hyphen, which reads as broken. German compounds in narrow card columns hit
    this constantly. Elements that opt into `hyphens: auto` are excluded: there
    the browser breaks at a real hyphenation point, which is correct.
    """
    return page.evaluate(
        """() => {
        const cx = document.createElement('canvas').getContext('2d');
        const out = [];
        for (const el of document.querySelectorAll(
                'h1,h2,h3,h4,h5,h6,p,li,dd,dt,blockquote,strong')) {
            if (el.classList.contains('visually-hidden')) continue;
            const own = [...el.childNodes].filter(n => n.nodeType === 3)
                                          .map(n => n.textContent).join(' ').trim();
            if (!own) continue;
            const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            if (cs.hyphens === 'auto') continue;
            cx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
            // A hyphen or slash is already a break opportunity, so the
            // unbreakable unit is the segment between them.
            const units = own.split(/[\\s\\u00a0]+/)
                             .flatMap(w => w.split(/(?<=[-\\u2013\\/])/));
            let worst = '', ww = 0;
            for (const u of units) {
                const m = cx.measureText(u).width;
                if (m > ww) { ww = m; worst = u; }
            }
            const avail = el.clientWidth - parseFloat(cs.paddingLeft)
                                         - parseFloat(cs.paddingRight);
            if (avail > 0 && ww > avail + 0.5) {
                out.push(`"${worst}" in ${el.tagName.toLowerCase()}.` +
                         String(el.className).trim() +
                         ` needs ${Math.round(ww)}px, has ${Math.round(avail)}px`);
            }
        }
        return [...new Set(out)].slice(0, 8);
    }"""
    )


def main():
    SHOTS.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for path in PAGES:
            url = BASE + path
            for vp_name, (w, h) in VIEWPORTS.items():
                ctx = browser.new_context(viewport={"width": w, "height": h})
                page = ctx.new_page()

                errors = []
                page.on("console", lambda m: errors.append(m.text)
                        if m.type == "error" else None)
                page.on("pageerror", lambda e: errors.append(str(e)))

                resp = page.goto(url, wait_until="networkidle")
                if resp.status != 200:
                    problems.append(f"{path} [{vp_name}] HTTP {resp.status}")

                # Settle the scroll-in animations. Their start state is
                # deliberately offset, which is not a layout defect -- the audit
                # is about where the page comes to rest.
                # Dropping `js-anim` switches the whole rule set off rather
                # than waiting out a 1.2s transition per element.
                page.evaluate(
                    "() => document.documentElement.classList.remove('js-anim')"
                )
                page.wait_for_timeout(60)

                ov = audit_overflow(page)
                if ov["docScroll"]:
                    problems.append(
                        f"{path} [{vp_name}] page scrolls horizontally; "
                        f"widest: {', '.join(ov['wide'][:3]) or 'n/a'}"
                    )
                for c in ov["clipped"]:
                    problems.append(f"{path} [{vp_name}] text clipped in {c}")
                for o in ov["overflowing"]:
                    problems.append(f"{path} [{vp_name}] overflows its box: {o}")

                for w in audit_wordfit(page):
                    problems.append(f"{path} [{vp_name}] word broken mid-word: {w}")

                for e in errors:
                    problems.append(f"{path} [{vp_name}] console: {e}")

                name = (path.strip("/").replace("/", "_") or "home")
                page.screenshot(
                    path=str(SHOTS / f"{name}__{vp_name}.png"),
                    full_page=(vp_name == "desktop"),
                )

                # link check once per page, on desktop only
                if vp_name == "desktop":
                    hrefs = page.eval_on_selector_all(
                        "a[href]", "els => els.map(e => e.getAttribute('href'))"
                    )
                    for href in set(hrefs):
                        if not href or href.startswith(("mailto:", "tel:", "#")):
                            continue
                        if urlparse(href).netloc and "localhost" not in href:
                            continue  # external, skip
                        target = urljoin(url, href)
                        status = check_link(page, target)
                        if status >= 400:
                            problems.append(
                                f"{path} → {href} returns HTTP {status}")

                ctx.close()

        # mobile nav interaction
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto(BASE + "/", wait_until="networkidle")
        toggle = page.locator(".nav-toggle")
        if toggle.is_visible():
            toggle.click()
            page.wait_for_timeout(400)
            if not page.locator("#site-nav").is_visible():
                problems.append("mobile: nav drawer did not open")
            else:
                page.screenshot(path=str(SHOTS / "home__mobile-nav-open.png"))
        else:
            problems.append("mobile: .nav-toggle is not visible at 390px")
        ctx.close()

        browser.close()

    print(f"\nChecked {len(PAGES)} pages × {len(VIEWPORTS)} viewports, "
          f"{len(checked_links)} unique links.\n")
    if problems:
        print(f"{len(problems)} problem(s):\n")
        for pr in problems:
            print("  -", pr)
        sys.exit(1)
    print("No problems found.")


if __name__ == "__main__":
    main()
