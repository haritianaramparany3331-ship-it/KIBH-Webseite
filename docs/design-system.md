# KIBH Design System — extracted from the live site

Source: `https://kiberatunghessen.com/wp-content/litespeed/css/e0b4791d69037a994ec588e17de987b4.css`
(Elementor global kit `.elementor-kit-10`). Values are read from the live
stylesheet, not estimated from screenshots.

---

## Colors

Elementor named globals:

| Token | Hex | Role |
|---|---|---|
| `primary` | `#31363F` | Dark slate — headings, dark surfaces |
| `secondary` | `#EEEEEE` | Light grey — section backgrounds |
| `text` | `#222831` | Near-black body text |
| `accent` | `#76ABAE` | **Teal** — buttons, links, highlights |

Additional palette entries in use:

| Hex | Notes |
|---|---|
| `#FFFFFF` | White |
| `#F8FAF9` | Off-white surface |
| `#EDF0EF` | Light neutral surface |
| `#D6D84F` | Yellow-green — secondary accent |
| `#77ABAE` | Near-duplicate of accent (off-by-one, likely unintentional) |
| `#587274` | Muted teal |
| `#3C6264` | Dark teal |
| `#1C3738` | Very dark teal |
| `#0D1D20` | Near-black teal |
| `#000F08` | Near-black green |
| `#222831 00` | Transparent variant of text color |

> Note: the brand accent is **teal `#76ABAE`**, not the light blue that a
> quick visual scan suggests. `#76ABAE` / `#31363F` / `#222831` / `#EEEEEE`
> is a widely-circulated stock palette.

---

## Typography

**Conflict worth flagging:** the Elementor global tokens declare
`Verdana` as the primary/secondary/text/accent family, but actual usage is
overwhelmingly **`Avenir`** — 68 direct `Avenir` declarations against 15 for
`Verdana`. Nearly every custom typography token specifies Avenir.

**Correction (2026-08-28).** An earlier version of this section claimed the
site had no `@font-face` rule and that Avenir therefore fell back to a
generic sans on Windows and Android. That was wrong. The site **self-hosts
Avenir**: `Avenir-Regular.ttf` and `Avenir-Heavy.ttf` are served from
`wp-content/uploads/2024/03/` and both load. Avenir renders for every
visitor on every OS, so there is no per-OS lottery, and the substitution
question is a licensing one rather than a rendering one — Avenir is a
licensed Linotype face we cannot serve ourselves. See "Open decisions".

### Type scale (desktop)

| px | Weight | Line-height | Typical use |
|---|---|---|---|
| 170 | 600 | 1 | Oversized display numeral |
| 64 | 600 | 1 | Hero headline |
| 52 | 600 | 1.1 | Major section headline |
| 48 | 600 | 1.1 | Section headline |
| 38 | 600 | 1 | Sub-headline |
| 32 | 600 | 1.2 | Card / block heading |
| 28 | 600 | 1.3 | Heading |
| 24 | 600 | 1.2 | Small heading |
| 20 | 600 | 1 | Label / lead-in |
| 20 | 500 italic | 1.6 | Quote / emphasis (`-0.02em` tracking) |
| 18 | 600 / 400 | — | Sub-heading / large body |
| 16 | 600 / 400 | 1.4 / 1.6 | Body, emphasized body |
| 15 | 600 | 1.4 | Small body |
| 14 | 400 | 1.6 | Caption |
| 12 | 600 uppercase | 1.4 | Eyebrow / overline |

Weights in use: **400, 500, 600**. No 700+ anywhere.

### Responsive type overrides

| Token | Desktop | Tablet (≤1024) | Mobile (≤767) |
|---|---|---|---|
| Body text | 16 | 16 | 15 |
| Hero (`ed980b4`) | 64 | 64 | 46 |
| Section (`1b49a19`) | 48 | 48 | 38 |
| Section (`217f77a`) | 52 | 52 | 38 |
| Display (`fa600a7`) | 48 | 34 | 38 |
| Numeral (`8cb63db`) | 170 | 170 | 140 |

---

## Layout

- **Content max-width:** `1140px` (Elementor default container)
- **Wide content width:** `1240px`
- **Breakpoints:** mobile `≤767px`, tablet `≤1024px`, desktop `≥1025px`
  (Elementor's standard three-tier set — confirmed by media-query
  frequency: 29× `max-width:1024px`, 26× `max-width:767px`)

---

## Open decisions for Stage 2

1. **Avenir substitution — RESOLVED 2026-08-28: Mulish.**

   Candidates were measured against the real Avenir files rather than
   chosen by reputation. Same headline, same size, width relative to
   Avenir:

   | Candidate | Heading width | Body width |
   |---|---|---|
   | **Mulish** | **100.2%** | **102.9%** |
   | Figtree | 96.7% | 99.8% |
   | Nunito Sans | 97.3% | 100.7% |
   | DM Sans | 103.2% | 101.3% |
   | Jost | 96.4% | 95.3% |
   | Poppins | 109.2% | 108.7% |
   | Montserrat | 111.8% | 110.2% |

   Overlaying each candidate on Avenir at 64px confirmed it: Mulish stays
   in register across a whole line, while Nunito Sans, Figtree and DM Sans
   visibly drift apart by the end of it.

   Body text is **Verdana**, matching the live site exactly — it is a system
   face on Windows and macOS, so it needs no webfont and raises no licence
   question at all.

   Still open for Willy: whether KIBH holds a webfont licence for Avenir. If
   it does, swapping Mulish for the real thing is a one-line token change.

2. **`#76ABAE` vs `#77ABAE`.** Almost certainly a typo in the original.
   Reproduce both, or normalise to one.
