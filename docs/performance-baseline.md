# Performance — WordPress vs. static rebuild

Homepage, Chromium, 1440×1000 viewport. Reproduce with `python tests/compare.py`
(dev server must be running).

| | Requests | Transferred | DOMContentLoaded | Load |
|---|---|---|---|---|
| **WordPress (live)** | 12 | 2 464 KB | 2 875 ms | 3 034 ms |
| **Static rebuild** | 5 | 101 KB | 79 ms | 240 ms |

**24.4× lighter, 7 fewer requests.**

### By resource type (KB)

| | document | stylesheet | script | font | image |
|---|---|---|---|---|---|
| WordPress | 202 | 1 363 | 310 | 496 | 93 |
| Static rebuild | 17 | 34 | 1 | 48 | 0 |

The stylesheet line is the headline: Elementor ships a single **1.36 MB**
combined stylesheet where the rebuild needs **34 KB**. Nearly all of that
1.36 MB is Elementor widget CSS for components this site never uses.

## Caveats — read before quoting these numbers

Three of these figures are not yet a fair fight, and the case study should
not present them as one:

1. **The timings compare localhost to the public internet.** No DNS, no TLS
   handshake, no network latency locally. The byte and request counts are a
   fair comparison; the millisecond figures are flattered and must be
   re-measured once the site is deployed to Vercel.
2. **Image weight is currently 0 KB** because every logo and photo is still a
   placeholder. Real assets will add weight. WordPress's 93 KB of images is
   the honest number to beat, and we should re-measure after upload.
3. **Fonts (re-measured 2026-08-28):** 29 KB, a single Mulish file. Body
   text is Verdana, a system face, so it costs nothing. The live site loads
   496 KB across 3 files — it self-hosts Avenir as uncompressed `.ttf`
   rather than `woff2`, which is most of the difference. 17x lighter.

Byte count and request count are the two numbers safe to quote today. Rerun
this script after deployment and after assets land, and replace the timing
row with the deployed figures.
