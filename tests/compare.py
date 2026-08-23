"""
Before/after comparison: live WordPress site vs. the local static rebuild.

Measures transferred bytes, request count, and time to DOMContentLoaded /
load for the homepage. Run with the dev server up:

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
    page.wait_for_timeout(2500)  # let deferred/lazy work settle

    timing = page.evaluate("""() => {
        const n = performance.getEntriesByType('navigation')[0];
        return n ? {dcl: Math.round(n.domContentLoadedEventEnd),
                    load: Math.round(n.loadEventEnd)} : null;
    }""")

    ctx.close()
    return stats, timing


def main():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for label, url in TARGETS:
            try:
                stats, timing = measure(browser, url)
                results.append((label, stats, timing))
            except Exception as e:
                print(f"  ! {label} failed: {e}")
        browser.close()

    print(f"\n{'':26} {'Requests':>9} {'Transferred':>13} {'DCL':>8} {'Load':>8}")
    print("-" * 68)
    for label, s, t in results:
        kb = s["bytes"] / 1024
        dcl = f"{t['dcl']} ms" if t else "n/a"
        load = f"{t['load']} ms" if t else "n/a"
        print(f"{label:26} {s['requests']:>9} {kb:>10.0f} KB {dcl:>8} {load:>8}")

    print("\nBreakdown by resource type (KB):")
    types = sorted({k for _, s, _ in results for k in s["by_type"]})
    header = f"{'':26}" + "".join(f"{t[:9]:>10}" for t in types)
    print(header)
    for label, s, _ in results:
        row = f"{label:26}" + "".join(
            f"{s['by_type'].get(t, 0)/1024:>10.0f}" for t in types)
        print(row)

    if len(results) == 2:
        a, b = results[0][1], results[1][1]
        if b["bytes"]:
            print(f"\nStatic rebuild is {a['bytes']/b['bytes']:.1f}× lighter "
                  f"and makes {a['requests'] - b['requests']} fewer requests.")


if __name__ == "__main__":
    main()
