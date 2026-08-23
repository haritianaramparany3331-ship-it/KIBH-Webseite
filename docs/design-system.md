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

**There is no `@font-face` rule and no Google Fonts link anywhere on the
site.** Avenir is a licensed Linotype face that ships with macOS but not
with Windows or Android. So on most visitors' machines the site is *already*
falling back to generic `Sans-serif`, and renders differently per OS. This
needs a decision in Stage 2 — see "Open decisions" below.

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

1. **Avenir substitution.** Options, in order of my preference:
   - **Nunito Sans** (Google Fonts, free) — geometric humanist, closest
     free match to Avenir's proportions and its 400/500/600 range.
   - **Montserrat** — more geometric, wider; recognisably different.
   - **System stack** (`-apple-system, Segoe UI, …`) — matches what most
     visitors *currently* see, but abandons the intended look on macOS too.

   Nunito Sans gives every visitor a consistent, close-to-intended result,
   which is arguably closer to design intent than today's OS lottery. A
   strict 1:1 reading would instead reproduce `font-family: "Avenir",
   Sans-serif` verbatim, fallback behaviour and all. **Flagging rather than
   deciding — this one is a judgement call about what "1:1" means.**

2. **`#76ABAE` vs `#77ABAE`.** Almost certainly a typo in the original.
   Reproduce both, or normalise to one.
