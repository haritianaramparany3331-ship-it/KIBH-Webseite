#!/usr/bin/env python
"""
Knock the flat background out of a photograph and write a WebP cut-out.

Why this exists rather than ImageMagick or `rembg`: same constraint as
tools/encode-webp.py. `package.json` has no dependencies, there is no PIL,
sharp or ImageMagick on this machine, and adding an image toolchain to the
project would undercut what the case study is arguing. Playwright is already
here for the test suites, and Chromium can read pixels and write WebP with an
alpha channel, so the whole thing runs in a canvas.

Method: a flood fill inward from the border, not a global threshold. The
subject this was written for -- Willy's reading robot -- is white but full of
near-black crevices, seams and shadow, and thresholding on darkness punched
holes straight through its chest and the gaps between its fingers. Filling
only from the edges removes background that is actually connected to the
outside and leaves enclosed dark areas alone.

Two corrections are applied afterwards, both of which matter on a black
ground:

  * the hard mask is blurred by a pixel or so, because a binary alpha edge
    reads as jagged against a lit background; and
  * the edge pixels are un-premultiplied. A pixel half-covered by the subject
    was photographed as a 50/50 blend with black, so leaving it as-is draws a
    dark fringe around the whole cut-out. Dividing the colour back out by the
    coverage recovers what the subject actually looked like there.

    python tools/cutout.py            # write the .webp
    python tools/cutout.py --dry-run  # report only, write nothing

Sources are removed once written, as encode-webp.py does, so that the copy of
`assets/` build.js drops into dist/ carries only files the site asks for. See
the note above JOBS for how to get one back out of git history.
"""

import base64
import mimetypes
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"

# source (relative to assets/img)  ->  settings
#
# Sources are deleted once their cut-out is written, the same way
# encode-webp.py treats its inputs, so that `assets/` -- which build.js copies
# to dist/ verbatim -- does not ship a master nobody requests. Git history
# keeps them; this one is at commit 7ea3dbd. Restore a source before re-running
# a job:  git show 7ea3dbd:"assets/img/DRE/Reading robot.jpg" > <path>
JOBS = {
    "dre/reading-robot.jpg": {
        "out": "dre/reading-robot.webp",
        # Max channel value still counted as background. Sampled: the ground
        # runs 1-23, so this sits just above it. 40 was tried first and let
        # the fill walk up dark seams into the fingers and the book.
        "tol": 28,
        # Opening radius on the background mask, in pixels. The shadowed side
        # of the book is genuinely as black as the ground -- median 6 against
        # the ground's 13 -- so no threshold can tell them apart, and the fill
        # threads into the subject through channels a few pixels wide. Opening
        # the background (erode, then dilate) deletes anything thinner than
        # this and leaves the real outer region untouched.
        "open": 3,
        # Alpha feather radius, in pixels.
        "feather": 1.5,
        # Longest edge of the output. Displayed around 420px tall, so this is
        # the 2x for retina; never upscaled past the source.
        "max_edge": 840,
        # Swept 0.70-0.90 against a 2x crop of the head, where the fine
        # panel seams are: all five were indistinguishable, so this takes
        # encode-webp.py's photograph default. 0.90 cost 123 KB, this 92.
        "quality": 0.82,
    },
}

CUTOUT = r"""async ([dataUrl, tol, openR, feather, maxEdge, quality]) => {
  const img = new Image();
  await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = dataUrl; });

  const W = img.naturalWidth, H = img.naturalHeight;
  const c = document.createElement('canvas');
  c.width = W; c.height = H;
  const x = c.getContext('2d', { willReadFrequently: true });
  x.drawImage(img, 0, 0);
  const id = x.getImageData(0, 0, W, H);
  const d = id.data;
  const N = W * H;

  // ---- 1. flood fill the background inward from the border ----------------
  const isBg = i => {
    const p = i * 4;
    return Math.max(d[p], d[p + 1], d[p + 2]) <= tol;
  };
  let mask = new Uint8Array(N);            // 1 = background
  const queue = new Int32Array(N);
  let head = 0, tail = 0;
  const push = i => { if (!mask[i] && isBg(i)) { mask[i] = 1; queue[tail++] = i; } };

  for (let px = 0; px < W; px++) { push(px); push((H - 1) * W + px); }
  for (let y = 0; y < H; y++) { push(y * W); push(y * W + W - 1); }

  while (head < tail) {
    const i = queue[head++];
    const px = i % W, y = (i - px) / W;
    if (px > 0)     push(i - 1);
    if (px < W - 1) push(i + 1);
    if (y > 0)      push(i - W);
    if (y < H - 1)  push(i + W);
  }

  // ---- 2. open the background, to drop leaks thinner than the radius ------
  // Min/max over a square structuring element are separable, so each pass is
  // two 1-D sweeps rather than a full neighbourhood scan.
  const rank1D = (src, k, wantMax) => {
    let cur = src;
    for (const horizontal of [true, false]) {
      const out = new Uint8Array(N);
      const outer = horizontal ? H : W, inner = horizontal ? W : H;
      for (let a = 0; a < outer; a++) {
        for (let b = 0; b < inner; b++) {
          let v = wantMax ? 0 : 1;
          const lo = Math.max(0, b - k), hi = Math.min(inner - 1, b + k);
          for (let t = lo; t <= hi; t++) {
            const val = cur[horizontal ? a * W + t : t * W + a];
            if (wantMax ? val > v : val < v) v = val;
          }
          out[horizontal ? a * W + b : b * W + a] = v;
        }
      }
      cur = out;
    }
    return cur;
  };
  if (openR > 0) {
    mask = rank1D(mask, openR, false);   // erode
    mask = rank1D(mask, openR, true);    // dilate back
  }

  let bgCount = 0;
  for (let i = 0; i < N; i++) if (mask[i]) bgCount++;

  // ---- 3. feather: separable box blur over the coverage -------------------
  const r = Math.max(0, Math.round(feather));
  let cov = new Float32Array(N);
  for (let i = 0; i < N; i++) cov[i] = mask[i] ? 0 : 1;

  const blur1D = (src, horizontal) => {
    const out = new Float32Array(N);
    const outer = horizontal ? H : W, inner = horizontal ? W : H;
    for (let a = 0; a < outer; a++) {
      let sum = 0;
      const at = b => horizontal ? a * W + b : b * W + a;
      for (let b = -r; b <= r; b++) sum += src[at(Math.min(inner - 1, Math.max(0, b)))];
      for (let b = 0; b < inner; b++) {
        out[at(b)] = sum / (2 * r + 1);
        const add = Math.min(inner - 1, b + r + 1), drop = Math.max(0, b - r);
        sum += src[at(add)] - src[at(drop)];
      }
    }
    return out;
  };
  if (r > 0) { cov = blur1D(cov, true); cov = blur1D(cov, false); }

  // ---- 4. un-premultiply the edge, then write the alpha -------------------
  // A pixel the subject only partly covers was captured as a blend with the
  // black ground. Without this every cut-out carries a dark outline.
  for (let i = 0; i < N; i++) {
    let a = cov[i];
    if (a <= 0.004) { d[i * 4 + 3] = 0; continue; }
    if (a < 0.999) {
      const p = i * 4;
      d[p]     = Math.min(255, d[p]     / a);
      d[p + 1] = Math.min(255, d[p + 1] / a);
      d[p + 2] = Math.min(255, d[p + 2] / a);
    }
    d[i * 4 + 3] = Math.round(a * 255);
  }
  x.putImageData(id, 0, 0);

  // ---- 5. crop to what is actually opaque ---------------------------------
  let x0 = W, y0 = H, x1 = -1, y1 = -1;
  for (let y = 0; y < H; y++) {
    for (let px = 0; px < W; px++) {
      if (d[(y * W + px) * 4 + 3] > 8) {
        if (px < x0) x0 = px;
        if (px > x1) x1 = px;
        if (y < y0) y0 = y;
        if (y > y1) y1 = y;
      }
    }
  }
  if (x1 < 0) throw new Error('everything was removed -- tolerance too high');
  const cw = x1 - x0 + 1, ch = y1 - y0 + 1;

  // ---- 6. scale to target and encode --------------------------------------
  const scale = Math.min(1, maxEdge / Math.max(cw, ch));
  const ow = Math.round(cw * scale), oh = Math.round(ch * scale);
  const out = document.createElement('canvas');
  out.width = ow; out.height = oh;
  const ox = out.getContext('2d');
  ox.imageSmoothingEnabled = true;
  ox.imageSmoothingQuality = 'high';
  ox.drawImage(c, x0, y0, cw, ch, 0, 0, ow, oh);

  return {
    url: out.toDataURL('image/webp', quality),
    src: W + 'x' + H,
    cropped: cw + 'x' + ch,
    out: ow + 'x' + oh,
    bgPct: Math.round(100 * bgCount / N),
  };
}"""


def main():
    dry = "--dry-run" in sys.argv
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        page = br.new_page()
        page.set_content("<!doctype html><meta charset=utf-8><title>cutout</title>")

        for rel, cfg in JOBS.items():
            src = IMG / rel
            if not src.exists():
                print(f"  MISSING  {rel}")
                continue
            mime = mimetypes.guess_type(src.name)[0] or "image/jpeg"
            data_url = "data:" + mime + ";base64," + base64.b64encode(src.read_bytes()).decode()

            res = page.evaluate(
                CUTOUT,
                [data_url, cfg["tol"], cfg["open"], cfg["feather"],
                 cfg["max_edge"], cfg["quality"]],
            )
            blob = base64.b64decode(res["url"].split(",", 1)[1])
            dst = IMG / cfg["out"]

            print(f"  {rel}")
            print(f"      source {res['src']}   background removed {res['bgPct']}% of frame")
            print(f"      cropped to {res['cropped']}   written at {res['out']}")
            print(f"      {len(src.read_bytes()) // 1024} KB -> {len(blob) // 1024} KB   -> {cfg['out']}")
            if not dry:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(blob)

        br.close()
    if dry:
        print("\n  --dry-run: nothing written")


if __name__ == "__main__":
    main()
