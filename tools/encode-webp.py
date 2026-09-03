#!/usr/bin/env python
"""
Re-encode the site's raster images to WebP, at the size they are displayed.

Why this exists rather than `sharp` or ImageMagick: `package.json` has no
dependencies and the build is plain Node, which is part of what the case study
is arguing for. Adding an image toolchain to get smaller images would undercut
that. Chromium already ships a WebP encoder, and Playwright is already here for
the test suites, so this draws each source into a canvas at the target size and
asks the browser to encode it:

    canvas.getContext('2d').drawImage(img, 0, 0, w, h)
    canvas.toDataURL('image/webp', QUALITY)

Alpha survives, so the logo cut-outs and round avatars keep their transparency.

Targets come from measuring the largest size each image is ever displayed at
(1440 / 768 / 390 viewports), doubled for retina and capped at the file's own
natural size -- there is no point encoding a 300px logo at 600px.

    python tools/encode-webp.py            # write the .webp files
    python tools/encode-webp.py --dry-run  # report only

The originals are deleted once written; git history keeps them.
"""

import os
import sys
import base64
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
# Photographs tolerate 0.82 without anything showing. Flat graphics that carry
# lettering -- the certificate, the TUV mark, the client logos and wordmarks --
# get a higher setting, because WebP's lossy mode softens hard edges and small
# type first, and those files are the ones a visitor reads rather than glances
# at. They are small either way, so the extra bytes cost nothing.
QUALITY = 0.82
QUALITY_GRAPHIC = 0.94
GRAPHIC = (
    "zertifikat", "tuev-rheinland", "logos/", "logo-", "wortmarke", "avatar-",
)

# path relative to assets/img  ->  (target width, target height)
# None means "keep the file's natural size".
TARGETS = {
    "startseite/zertifikat-ai-consultant.png": (1440, 1012),
    "startseite/tuev-rheinland-pruefzeichen.png": (1440, 532),
    "startseite/willy-li.png": (1376, 1370),
    "erechnung/image-1.png": (1440, 1800),
    "erechnung/image-2.png": (1440, 916),
    "erechnung/image-3.png": (1440, 916),
    "erechnung/image-4.png": (1440, 916),
    # A `cover` background on the E-Rechnung hero and closing band, so it is
    # sized to the widest viewport it has to fill rather than to a box.
    "erechnung/bg-1.png": (1920, None),
    "ergebnisse/rechnungspruefung-bauwesen.png": None,
    "ergebnisse/til-steinhauer.jpg": (240, 240),
    "ergebnisse/torsten-krueger-square.jpg": (240, 240),
    "ergebnisse/torsten-krueger.jpg": (240, 240),
    "ergebnisse/logo-entropia.png": (86, 30),
    "ergebnisse/logo-business-elegance.png": (86, 72),
    "ergebnisse/hinnerbaecker-wortmarke.jpg": (220, 82),
    "ergebnisse/avatar-zrakic.png": None,
    "ergebnisse/avatar-newway.png": None,
    "startseite/logos/1-hinnerbaecker.png": (288, 288),
    "startseite/logos/2-zrakic.png": (288, 288),
    "startseite/logos/3-wonderland.png": (288, 288),
    "startseite/logos/4-u2care.png": (288, 288),
    "startseite/logos/5-jj-real-estate.png": (288, 288),
    "startseite/logos/6-newway.png": (288, 288),
    "startseite/logos/7-ihk.png": (288, 288),
}

# Deliberately untouched:
#   startseite/hero-robot.png  -- Hari asked for the hero to be left alone
#   kibh-logo.png              -- 10 KB, and it is the brand mark
#   *.svg                      -- already smaller than any raster would be
#   *.webp                     -- already done

ENCODE = """async ([dataUrl, tw, th, quality]) => {
    const img = new Image();
    await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = dataUrl; });
    let w = tw || img.naturalWidth, h = th || img.naturalHeight;
    // Never upscale: a source smaller than the target stays at its own size.
    const scale = Math.min(1, w / img.naturalWidth, th ? h / img.naturalHeight : 1);
    w = Math.round(img.naturalWidth * scale);
    h = Math.round(img.naturalHeight * scale);
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const x = c.getContext('2d');
    x.imageSmoothingEnabled = true;
    x.imageSmoothingQuality = 'high';
    x.drawImage(img, 0, 0, w, h);
    return { url: c.toDataURL('image/webp', quality),
             w, h, nw: img.naturalWidth, nh: img.naturalHeight };
}"""

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def main():
    dry = "--dry-run" in sys.argv
    before = after = 0
    rows = []

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        page = br.new_page()
        page.set_content("<!doctype html><meta charset=utf-8><title>encoder</title>")

        for rel, target in TARGETS.items():
            src = IMG / rel
            if not src.exists():
                print(f"  MISSING  {rel}")
                continue
            raw = src.read_bytes()
            data_url = ("data:" + MIME[src.suffix.lower()] + ";base64,"
                        + base64.b64encode(raw).decode())
            tw, th = target if target else (None, None)
            q = QUALITY_GRAPHIC if any(g in rel for g in GRAPHIC) else QUALITY
            out = page.evaluate(ENCODE, [data_url, tw, th, q])
            blob = base64.b64decode(out["url"].split(",", 1)[1])

            dst = src.with_suffix(".webp")
            before += len(raw)
            after += len(blob)
            rows.append((rel, len(raw), len(blob), out["nw"], out["nh"], out["w"], out["h"], q))
            if not dry:
                dst.write_bytes(blob)
                if src.suffix.lower() != ".webp":
                    src.unlink()
        br.close()

    w = max(len(r[0]) for r in rows) + 2
    print(f"  {'file':{w}}{'before':>9}{'after':>9}{'saved':>8}  q     dimensions")
    for rel, b, a, nw, nh, ow, oh, q in rows:
        pct = 100 * (1 - a / b) if b else 0
        dim = f"{nw}x{nh}" + (f" -> {ow}x{oh}" if (ow, oh) != (nw, nh) else "")
        print(f"  {rel:{w}}{b/1024:>8.0f}K{a/1024:>8.0f}K{pct:>7.0f}%  {q}   {dim}")
    print(f"\n  {len(rows)} files: {before/1024:.0f} KB -> {after/1024:.0f} KB "
          f"({100 * (1 - after / before):.0f}% smaller)"
          + ("   [dry run, nothing written]" if dry else ""))


if __name__ == "__main__":
    main()
