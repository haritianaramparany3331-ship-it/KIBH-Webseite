# Performance — WordPress vs. static rebuild

Homepage, Chromium, 1440×1000 viewport. Reproduce with `python tests/compare.py`
(dev server must be running). Measured 2026-09-03, after the images were
re-encoded to WebP.

The page is measured **twice**, because the two figures answer different
questions and quoting only one of them would mislead. Both sites lazy-load
images, so the second measurement scrolls to the bottom — otherwise the
comparison flatters us by counting only what arrives before the visitor moves.

## On load — what arrives before the visitor does anything

| | Requests | Transferred |
|---|---|---|
| **WordPress (live)** | 12 | 2 464 KB |
| **Static rebuild** | 16 | 362 KB |

**6.8× lighter.**

## Fully read — what a visitor who reads the page downloads

| | Requests | Transferred |
|---|---|---|
| **WordPress (live)** | 21 | 2 735 KB |
| **Static rebuild** | 20 | 621 KB |

**4.4× lighter.**

### By resource type, fully read (KB)

| | document | stylesheet | script | font | image |
|---|---|---|---|---|---|
| WordPress | 202 | **1 363** | 310 | 496 | 365 |
| Static rebuild | 32 | **126** | 22 | 29 | 412 |

The stylesheet line is where the difference really is: Elementor ships a single
**1.36 MB** combined stylesheet, nearly all of it widget CSS for components this
site never uses, against **126 KB** here. Scripts are 14× lighter and fonts 17×,
because the rebuild loads one webfont file from Google Fonts — Mulish, since
Verdana is a system face and costs nothing — where WordPress self-hosts Avenir
as uncompressed `.ttf`. Every page carries the same 29 KB; before Plus Jakarta
Sans was dropped, E-Rechnung and the four case pages carried 56 KB.

**Images are the one line WordPress still wins**, 365 KB against 412 KB, and it
is worth being straight about why: WordPress generates `srcset` variants at half
a dozen widths and serves whichever fits the viewport, where the rebuild serves
one file per image. Closing that last gap would mean generating a `srcset` set
here too. It is the obvious next step if the number ever needs to be larger, and
it is not currently worth the complexity.

## Per page, fully scrolled

| page | transferred |
|---|---|
| `/` | 614 KB |
| `/e-rechnung/` | 426 KB |
| `/ergebnisse/` | 252 KB |
| `/ergebnisse/automatische-rechnungspruefung/` | 222 KB |
| `/ergebnisse/u2care/` | 198 KB |
| `/deep-reading-engine/`, `/kontakt/`, `/impressum/`, `/vertraulichkeit/` | ~192 KB |

Reproduce with `python scratchpad/look/weight2.py`.

## How the images got there

`assets/img` went from **6.6 MB to 789 KB** — 25 files re-encoded to WebP at the
size they are actually displayed (largest rendered size across 1440 / 768 / 390,
doubled for retina, never upscaled past the source). Photographs at quality
0.82, flat graphics carrying lettering at 0.94, because lossy WebP softens hard
edges and small type first, and the hero at 0.90 — it is the largest single
image and it is upscaled on a retina display, so it gets more headroom.

`tools/encode-webp.py` does it with **no build dependency**: `package.json` still
has none. Chromium already ships a WebP encoder and Playwright is already here
for the test suites, so the script draws each source into a canvas at the target
size and calls `canvas.toDataURL('image/webp', q)`. Alpha survives, so the logo
cut-outs and round avatars keep their transparency.

Verified against full-page screenshots of all 12 pages at 1440 and 390 before
and after: every page identical in height bar one pixel on `/e-rechnung/` at
390px, and that came from correcting `width`/`height` attributes that had never
matched their files (`image-1` was declared 399×499 for a 640×800 image), which
removes a small layout shift rather than adding one.

## Caveats — read before quoting these numbers

1. **The timings are not a fair fight and are deliberately not quoted above.**
   The rebuild is measured on localhost — no DNS, no TLS handshake, no network
   latency — against a live site over the internet. Byte counts and request
   counts are fair; milliseconds are not. Re-measure once the site is deployed
   to Vercel and only then put a speed figure in front of a client.
2. **Both figures move when content changes.** These were taken with the real
   imagery in place, which is what makes them usable — the previous version of
   this document claimed 24.4× on a build where every image was still a
   placeholder and the image row read 0 KB. That number was never true of the
   finished site and should not be reused.
3. Request counts are close (20 vs 21 fully read) and are not the story. Bytes
   are.
