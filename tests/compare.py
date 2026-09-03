"""
Before/after comparison: live WordPress site vs. the local static rebuild.

Measures the homepage twice, because the two figures answer different
questions and quoting only one of them would mislead:

  * on load     -- what arrives before the visitor does anything. Neither site
                   has fetched its lazy images at this point.
  * fully read  -- after scrolling to the bottom, which is what a visitor who
                   actually reads the page downloads. Both sides lazy-load, so
                   both have to be scrolled or the comparison flatters us.

Run with the dev server up:

    python tests/compare.py
"""

from playwright.sync_api import sync_playwright

TARGETS = [
    ("WordPress (live)", "https://kiberatunghessen.com/"),
    ("Static rebuild (local)", "http://localhost:4173/"),
]


def measure(browser, url):
    ctx = browser.new_context(viewport={"width": 1440, "height": 1000})
    page = ctx.new_page()

    stats = {"requests": 0, "bytes": 0, "by_type": {}}

    def on_response(resp):
        stats["requests"] += 1
        try:
            body = resp.body()
        except Exception:
            return
        rtype = resp.request.resource_type
        stats["bytes"] += len(body)
        stats["by_type"][rtype] = stats["by_type"].get(rtype, 0) + len(body)

    page.on("response", on_response)
    page.goto(url, wait_until="load", timeout=90_000)
    page.wait_for_timeout(2500)  # let deferred work settle

    timing = page.evaluate("""() => {
        const n = performance.getEntriesByType('navigation')[0];
        return n ? {dcl: Math.round(n.domContentLoadedEventEnd),
                    load: Math.round(n.loadEventEnd)} : null;
    }""")
    on_load = {"requests": stats["requests"], "bytes": stats["bytes"],
               "by_type": dict(stats["by_type"])}

    # Walk the whole page so every lazy image on both sides actually loads.
    page.evaluate("""() => new Promise(r => { let y = 0;
        const step = () => { window.scrollTo(0, y); y += innerHeight;
          if (y < document.body.scrollHeight + innerHeight) setTimeout(step, 120);
          else { window.scrollTo(0, 0); setTimeout(r, 1200); } };
        step(); })""")
    page.wait_for_timeout(2500)

    ctx.close()
    return on_load, stats, timing


def main():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for label, url in TARGETS:
            try:
                on_load, full, timing = measure(browser, url)
                results.append((label, on_load, full, timing))
            except Exception as e:
                print(f"  ! {label} failed: {e}")
        browser.close()

    for title, idx in (("ON LOAD", 1), ("FULLY READ (scrolled to the bottom)", 2)):
        print(f"\n{title}")
        print(f"{'':26} {'Requests':>9} {'Transferred':>13} {'DCL':>8} {'Load':>8}")
        print("-" * 68)
        for row in results:
            label, s, t = row[0], row[idx], row[3]
            dcl = f"{t['dcl']} ms" if t else "n/a"
            load = f"{t['load']} ms" if t else "n/a"
            print(f"{label:26} {s['requests']:>9} {s['bytes']/1024:>10.0f} KB "
                  f"{dcl:>8} {load:>8}")
        if len(results) == 2 and results[1][idx]["bytes"]:
            a, b = results[0][idx], results[1][idx]
            print(f"  -> rebuild {a['bytes']/b['bytes']:.1f}x lighter, "
                  f"{a['requests'] - b['requests']:+d} requests")

    print("\nFully-read breakdown by resource type (KB):")
    types = sorted({k for r in results for k in r[2]["by_type"]})
    print(f"{'':26}" + "".join(f"{t[:9]:>10}" for t in types))
    for label, _, full, _ in results:
        print(f"{label:26}" + "".join(
            f"{full['by_type'].get(t, 0)/1024:>10.0f}" for t in types))


if __name__ == "__main__":
    main()
