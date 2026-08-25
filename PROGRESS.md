# PROGRESS

Log of what has been done, session by session. Goal, rules and tech stack are
in `CLAUDE.md` — not repeated here.

Read this at the start of a session. Append a new dated entry at the end of one.
Newest at the bottom. Short lines.

## Commands

- `npm run dev` — build + serve on `http://localhost:4173`
- `npm run build` — `src/` → `dist/`
- `python tests/qa.py` — Playwright QA, 11 pages x 5 viewports
- `python tests/compare.py` — perf comparison vs. the live WordPress site
- Run Python through the Bash tool. `python.exe` is not on the PowerShell PATH.
- Live: https://kibh-webseite.vercel.app — Vercel deploys on push to `main`. Working.

## 2026-08-23 — Stage 1, foundations

1. `git init`, `.gitignore`, directory structure.
2. Design system extracted from the live Elementor kit into CSS custom properties → `docs/design-system.md`.
3. Old WordPress URL structure mapped → `docs/url-map.md`.
4. Content inventory of the live site + list of its defects → `docs/content-inventory.md`.
5. Willy's raw DRE drafts stored → `docs/content-deep-reading-engine.md`.
6. Commits `4f251fd`, `c8f75eb`.

## 2026-08-23 — Stage 2, 1:1 rebuild

1. Build system written: `build.js` reads `src/pages/*.html` + `src/partials/`, writes `dist/`. Pages carry a JSON front-matter comment (`title`, `description`, `url`).
2. All 10 pages rebuilt faithfully: Startseite, E-Rechnung, Ergebnisse + 4 subpages, Kontakt, Impressum, Vertraulichkeit, plus a 404.
3. Shared header/footer partials, `assets/css/main.css`, `assets/js/main.js`.
4. Placeholder images throughout.
5. `vercel.json`: build config, `cleanUrls`, `trailingSlash`, `/index.php/*` redirects from the old URLs.
6. QA suite `tests/qa.py` written and green.
7. Performance measured vs. live WordPress → `docs/performance-baseline.md`. 101 KB vs 2 464 KB, 24x lighter.
8. Commits `4dda33b`, `e3b02ff`.

## 2026-08-24 — Stage 3, Deep Reading Engine

1. New page `/deep-reading-engine/`, built by merging and polishing Willy's three overlapping drafts.
2. Reuses only existing components — no new design language.
3. Entry points: nav, footer, dark teaser band on the homepage.
4. Nav drawer breakpoint moved 900px → 1024px. The 5th nav item was pushing the CTA off-screen.
5. Commit `196fe93`, pushed.

## 2026-08-24 — cleanup pass

1. All 18 emoji card icons removed site-wide. `.card__icon` CSS deleted.
2. 16 German text-fitting defects fixed: hero `clamp()`, `blockquote` UA margin, `.grid--4` column counts, `.pillar` padding, hyphenation limits.
3. `audit_wordfit()` added to `tests/qa.py` — catches this class of bug automatically from now on.
4. `laptop` and `tablet-sm` viewports added to QA. The old 390/900/1440 set had a blind spot.
5. Commit `e572b86`, pushed.

## 2026-08-25 — housekeeping, nav order, first E-Rechnung rebuild

1. `PROGRESS.md` created, then restructured as a dated log. Commits `869b284`, `e7d01bb`.
2. Nav order swapped: Deep Reading Engine is now second, E-Rechnung third. Header and footer. Commit `1e606fe`.
3. E-Rechnung rebuilt against the live page structure: dark hero, consequence tiles, questions band, image + icon list, two solution cards, Große/Kleine tab group. Commit `ddc4bbf`.
4. Text taken verbatim from the live page, including its own typos ("Manuellen Mehraufwand", "her– oder", "KI-Exzellence"). Those are for the copy pass, not for a rebuild.

## 2026-08-26 — E-Rechnung visual 1:1

Hari's rule for this page only: 1:1 means what a visitor sees, not the DOM.
Verified by driving both pages with Playwright, not by reading markup.

1. Typeface. The live E-Rechnung page is Plus Jakarta Sans, not Nunito Sans. Scoped to this page's `<main>` via `bodyClass`, so every other page is untouched.
2. Measure. The original lays out on 1140px content width, not our 1240px container. Cards 560px, tabs 569/571, images 550×350.
3. Entrance animations added: blocks fade up, images slide in from their own side. IntersectionObserver + `js-anim` class, reduced-motion honoured, nothing hidden with JS off. Button hovers 0.3s, matching the original.
4. Page assets pulled from the live site into `assets/img/erechnung/` — hero artwork, drawn underline, blurred shape, four photos. Only way to be visually 1:1.
5. Type scale, alignment and icon sizes taken from measurements: 44/46px headings, 40/42/38px icons, tighter line-heights.
6. "Die Vorteile" is a 400/700 image + icon-list split, not a card grid.
7. Commit `5c2d617`.
8. Fixed: browser default `figure { margin: 1em 40px }` pushed images 24px past their grid column.
9. Fixed: `vercel.json` served `/assets/*` with a one-year `immutable` cache while `main.css` / `main.js` never changed name, so returning visitors never saw a deploy. Build now emits `main.<sha1>.css` / `main.<sha1>.js`. Commit `4b800da`.
10. Three bands — "Was bedeutet das konkret für Sie?", "Unsere Lösungen", the closing CTA — are designed black with a neon bloom. The live site has lost their background, so their white type renders on white and they look empty. I first copied that as-is; corrected. `ss.svg` is drawn with `mix-blend-mode: plus-lighter`, which only works on a dark ground — that is the proof. Commit `8ecbc81`.
11. `tests/qa.py` now settles animations before auditing and skips `aria-hidden` decoration.

## Open — waiting on Hari

- Real assets: logos, team photos, client logos. Placeholders everywhere except E-Rechnung.
- E-Rechnung reuses the live site's own photos and artwork. Confirm that is fine or ask for placeholders back.
- The closing E-Rechnung CTA has no logo image; the original has one there.
- The 🙂 inside Martin Kraus's quoted testimonial on `/ergebnisse/`. Left in — it is a customer's own words.

## Open — waiting on Willy

- Which DRE draft framing is authoritative.
- Draft 3's third use case cuts off mid-sentence after "Angebot".
- Booking backend for "Kostenloses Erstgespräch": Calendly embed vs. serverless form.
- Kommunikation page has 3 empty section headings — keep or fill?
- Impressum was translated to German. Live site had it half in English. Confirm or revert.

## Deferred

- Full copy-polish pass over every text.
- Phase 3 workflow documentation.
- Phase 4 B2B case study: PDF handout + embeddable HTML.
