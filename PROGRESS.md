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

## 2026-08-27 — Deep Reading Engine, Willy's final text

1. `docs/content-deep-reading-engine.md` replaced with Willy's final text. The three overlapping drafts are gone — this supersedes them.
2. `/deep-reading-engine/` rebuilt around that text word for word: dark hero, "Das Geheimnis liegt in unserer Architektur" with 4 pillar cards, "Reale Anwendungsbeispiele" with 3 case cards on a dark teal band, closing CTA.
3. Copy fidelity checked mechanically, not by eye: source doc vs. rendered page, whitespace normalised, bullets stripped — 2 755 chars, identical.
4. Motion and icon CSS lifted out of the E-Rechnung block into a shared "Motion & icons" section. The DRE page reuses it — same fade-up entrances, same hover lift.
5. Commit `a4309b4`.
6. Grammar pass on Willy's text, after Hari allowed it: `KI workflows` → `KI-Workflows`, `weißt dass` → `weiß, dass`, `verständniss` → `Verständnis`, `Know-How` → `Know-how`, `Mit unsere` → `Mit unserer`, `in eine vielzahl` → `in einer Vielzahl`, `statt blind halluziniert` → `statt blind zu halluzinieren`, `1.Ausschreibungen` → `1. Ausschreibungen`, plus noun capitalisation and the closing quote. Applied to the doc and the page together.
7. `z.B.` kept without a space, on Hari's instruction.
8. Homepage teaser now carries Willy's own title and lead sentence instead of the old summary. Commit `9a97e34`.
9. Closing CTA: first tried the E-Rechnung style band ("KI Beratung Hessen / Ihr Weg zur KI-Exzellenz"), then reverted to the question form Hari preferred — "Haben Sie ein Dokument, an dem KI bisher gescheitert ist?" + Termin buchen. Commit `6b208ed`.
10. Trap found and documented in the CSS: `[data-anim].is-in { transform: none }` is specificity 0,3,0 and silently beat `.dre-pillar:hover` at 0,2,0, so the hover lift did nothing. Fixed by putting the reveal on a wrapper and the hover on the card.
11. webapp-testing on the DRE page at 390/768/900/1040/1440: no unrevealed animations, no console errors, no overflow. Full QA suite green, 11 pages × 5 viewports.
12. Pushed. Live and serving `main.eb48b99b.css`.

## 2026-08-28 — client recommendations on Ergebnisse

1. `docs/content-recommendations.md` created for Willy's four new recommendations — Volker Adelfinger, Mihaela Geiger, Daniel Markus, Jarne Van Gompel. Same role as the DRE content doc: verbatim source, extend at the bottom.
2. Text is final and untouched, typos included (`alltagfunktionierende`, `TipTop!`). No grammar pass this time — Hari said it was already reviewed.
3. New card variant `.case--reco`: quote, round avatar, name | role, company. No heading above, no "Mehr lesen" below, because these have no detail page.
4. The avatar circle came from looking at the live WordPress cards, which carry a 64px round company logo our rebuild had dropped. Placeholder for now.
5. Added to `/ergebnisse/` only. The homepage stays a 3-card teaser — that is what its "weitere Success Stories" button is for. Hari's call.
6. Jarne Van Gompel now appears twice on the page, once per project. Also Hari's call, both quotes stay.
7. Commit `a9fd894`.
8. Martin Kraus moved out of his standalone quote band and into the grid as a card, ahead of the new ones. Quote verified byte-identical after the move, 873 chars.
9. Grid went to 11 cards and ended on a half-empty row. First fix stretched the last card via `:nth-child` arithmetic. Commit `d0d5cc8`.
10. Then Martin went full width, because his testimonial runs 4× longer than its rowmates and left them mostly empty — his row dropped 682px → 298px.
11. That broke the `:nth-child` fill rule: it counts children, and Martin now occupies 3 slots. Replaced with explicit `.case--wide` / `.case--close` spans. Commit `cb92ddb`.
12. `.grid--testimonials` pins its own column counts (1 / 2 from 600px / 3 from 912px, measured by bisection) instead of leaving them to `auto-fit`. Column-span maths is only correct if the column count is known.
13. Fixed: `flex-grow` sat on the quote box, so a short quote next to a long one had its accent rule dragged down through empty space. Moved to `.case__person`.
14. Verified every grid row sums to the full grid width at 1, 2 and 3 columns. Card copy checked against the source doc mechanically at 5 viewports — identical. Full QA green.
15. Pushed, live, `main.aa817137.css`.

## 2026-08-28 — typefaces, then the homepage rebuilt against the original

1. Typeface pair corrected site-wide. The live site is Verdana for running text and Avenir for headings, nav and buttons. We had been on Nunito Sans throughout. Avenir is licensed and cannot be self-served, so headings use Mulish — picked by measuring candidates against the real Avenir files, not by reputation: it sets the same headline at 100.2 % of Avenir's width and stays in register across a line, where Nunito Sans, Figtree and DM Sans all drift. Commit `b1b1c11`.
2. Homepage deep-audited against the original section by section with Playwright, then rebuilt. Commit `60fb6e2`.
3. Rule Hari set for the audit: any sentence without an exact match on the original is replaced with the original's wording, word for word. A checker script walked every text run on our page and looked it up in the live page's text — 102 runs, the 20 unmatched all explained (asset placeholders, the approved DRE band, one added comma).
4. Weights. The original asks for 600 but ships Avenir 400/700 only, so every heading on it actually renders bold. Mulish has a real 600, which is visibly lighter — `.page-home` headings, eyebrows, buttons and authors go to 700.
5. Colours sampled from the live page instead of guessed: `#0D1D20` hero, `#000F08` solutions headline and card titles (the "black" one), `#31363F` other section headlines, `#222831` body, `#587274` hero lead.
6. Three whole sections were structurally wrong and only showed up in rendered crops, not in computed styles: the three process steps are staggered white panels joined by dotted connectors, "Warum wir?" is a two-column block with certificates on the left, and the team photos sit above the names rather than beside them.
7. Solution-card hover established by pixel-diffing a genuinely visible card: the card floods to the accent colour, text to `#EEEEEE`, icon chip to lime, 0.4s. Reading the `::before` had been misleading — it is vestigial and transparent.
8. Entrance animations added throughout, matching the original's Elementor `fadeInUp` / `fadeInLeft` / `fadeInRight`. Hero underline is the original's own SVG path, drawn on with the reveal.
9. Placeholder circles added for the two team photos and the two "Warum wir?" certificates.
10. Fixed along the way: `.member__photo` overflowing at mobile, "Geschäftsführer" breaking mid-word at laptop, the testimonials button colliding with the logo strip, and the hero underline crossing the descender of "g" — Mulish's content box is 1.047em against Avenir's 1.203em, so the same percentage lands differently.

## 2026-08-29 — Ergebnisse rebuilt, legal pages taken from the original

1. Fixed: two lime underlines were rendering under "KI-Lösungen" — an older flat-bar `::after` had been left in the stylesheet beside the SVG stroke that replaced it. Commit `39e2118`.
2. Ergebnisse compared against `https://kiberatunghessen.com/index.php/ergebnisse/` and rebuilt. Commit `f8852a8`.
3. Invented lead sentence under the page heading removed ("Ausgewählte Projekte aus Mittelstand, Bauwesen…"). A text diff confirms the only other copy changes are the placeholder labels and `Mehr lesen` → `Mehr Lesen`, the original's own capitalisation.
4. Card chrome from the original: white, 4px radius, `rgba(0,0,0,.15) 3px 0 12px`, 20px padding, 20px gutter, on the `#f8faf9` band. Quote, avatar and attribution now share the original's tinted `rgba(118,171,174,.314)` panel instead of an italic pull-quote with an accent rule.
5. Container widened to hold 1140px of content, so the columns come out at the original's 367px and the copy breaks over the same lines.
6. Intros carry the metric in bold, as on the original. Placeholder circles for the six missing client photos, plus a 327×280 slot for the project photo on the Rechnungsprüfung card.
7. Animation: the original plays exactly one `fadeInUp` over the whole cards band — checked across all 21 `data-settings` widgets and the raw HTML. It has no card hover at all; pixel-diffing a hovered card gave byte-identical screenshots. The inherited card lift was removed accordingly, since our cards are not clickable.
8. Fixed: long job titles ("Angebotsvergleich", "Softwareentwickler") overflowed the ~160px attribution column between 912px and 1100px. Hyphenation with `hyphenate-limit-chars: 10 5 4`, so it breaks as `Angebots-vergleich`.
9. Closing CTA band dropped — the original ends on the last card and runs into the footer. Commit `8a12214`.
10. Fixed: the tinted panel is pushed to the foot of the card, so on the card with the longest intro the slack ran out and the two touched. 26px bottom margin on the intro as a floor — the tightest that gap ever gets on the original. Commit `2d4ac6c`.
11. Card titles unified at 26px bold on Hari's call. The original sizes each one individually (32/28/27/22px) so each fits a line, which reads as six different headings. 26px is the largest that still fits the longest one-line title. Two lines are reserved for every title so the one that wraps keeps its intro level with its rowmates'. Commit `db582ce`.
12. Page hero given the Deep Reading Engine hero's treatment on Hari's call — same ink ground with its two accent blooms, 56px/1.1, accent eyebrow, lit hairline at the bottom edge. Commit `0f709f9`.
13. Potenzial Analyse, Kommunikation / Management, U2care and Automatische Rechnungsprüfung removed from the footer quicklinks. One edit in the shared partial, verified on all 12 pages. They stay in the nav dropdown. Commit `66e3cff`.
14. Impressum and Vertraulichkeit taken from the live pages word for word. Commit `6ebb486`.
15. Impressum had been rewritten into a German TMG layout; it now carries the original's own English headings and mixed-language address block. Four drifts fixed in Vertraulichkeit: two spaces before an ellipsis, a shortened cnil.fr link label, and a subhead under 8. that had been cut off mid-sentence.
16. Layout, hierarchy and the site's Mulish/Verdana pair stay ours — Hari prefers our design on these two pages, only the text is 1:1. A block-by-block diff script against both live pages reports every block matching.
17. Fixed: the first element inside `.prose` stacked its own top margin on the section padding, leaving a ~144px hole under the page hero.
18. `scratchpad/verify_erg.py` written as the Ergebnisse acceptance pass — 5 viewports, animation reveal, overflow, clipped text, even card heights, weight/colour/geometry table, hover. Green. Full QA suite green throughout, 11 pages × 5 viewports.

## 2026-08-29 — Kontakt page

1. Structure confirmed on the live page before building, not assumed: "Termin Buchen" and "Erstmal Kontakt aufnehmen" are two Elementor nested tabs on ONE page, `flex-direction: column-reverse`, so the strip renders below the panel it controls. Under 768px it flips to `column` with full-width buttons. Commit `f4b13f7`.
2. Tab 1 holds a Calendly embed (`calendly.com/ilya-den-volkov/kostenlose_strategieanalyse`, 700px). Our booking placeholder stays in its place — still no backend.
3. Tab 2 holds the contact form: Name / Telefon / Email / Nachricht, Senden. Labels exist but are `elementor-screen-only`; a sighted visitor sees only placeholders. Reproduced with `.visually-hidden`.
4. Headline is Elementor's animated headline in `typing` mode. Its own `data-settings` gave the three phrases verbatim — "deine Arbeit zu erleichtern." / "dich kennen zu lernen." / "zusammen zu arbeiten." — plus `rotate_iteration_delay: 2500`. Static half `#31363F`, rotating half accent, 1px blinking caret. The widget does not run in headless Chromium, so typing/erasing speeds are ours; the hold is the original's.
5. Measurements taken rather than guessed: tabs `#CECCCC`/`#EEEEEE` idle → `#76ABAE`/white on hover and when active, 15px 35px, Verdana 16px 400, 10px gap, 0.3s. Form panel `#FCFCFC`, 1px `#DADADA`, 4px radius, 45px padding; fields 44px, textarea 114px (4 rows), button 54px. Ours land on the same numbers.
6. No backend: `form[data-inert]` + a submit handler that calls `preventDefault()`. Without it a form with no action posts the page to itself and looks like a successful send.
7. Removed on Hari's instruction: the "So läuft das Erstgespräch ab" section — checked first, it is nowhere on the original, not in the page flow and not in a popup. Also removed the eyebrow and the lead paragraph, both invented.
8. The live page has no entrance or scroll animations at all (0 `elementor-invisible`, one animation setting and it is the headline). None added.
9. `scratchpad/cta_audit.py`: every booking CTA on all 12 pages resolves to `/kontakt/`, the target returns 200, and the header button was clicked through from three separate pages. The one exception is E-Rechnung's "Beratung zur E-Rechnungspflicht buchen", an in-page jump on the original too (`#solutions` there).
10. Fixed: the Ergebnisse container override was unscoped and beat `.container--wide`, so the header and footer sat 52px narrower on that page than on every other one. Scoped to `<main>`.
11. Fixed: the rotating phrase is held together with non-breaking spaces, so at a fixed 32px it is 409px wide and pushes a phone into horizontal scroll — the original does this too (scrollWidth 421 at 390px). Headline is fluid below ~500px, and the reservation width is re-measured on resize.
12. `scratchpad/verify_kontakt.py`: 5 viewports, tab switching both ways, strip position per breakpoint, keyboard arrows, hover, field geometry, submit does not navigate, headline actually types, and a six-way text diff against the live page. Green. Full QA suite green.

## Open — waiting on Hari

- Real assets: logos, team photos, client logos. Placeholders everywhere except E-Rechnung.
- Photos for the 5 recommendation-card avatars on `/ergebnisse/`. Dashed „Foto“ circles until then.
- The 6 older case cards on `/ergebnisse/` still have no avatar; the live site gives them one. Needs the real logos.
- E-Rechnung reuses the live site's own photos and artwork. Confirm that is fine or ask for placeholders back.
- The closing E-Rechnung CTA has no logo image; the original has one there.
- The 🙂 inside Martin Kraus's quoted testimonial on `/ergebnisse/`. Left in — it is a customer's own words.

## Open — waiting on Willy

- Booking backend for "Kostenloses Erstgespräch": Calendly embed vs. serverless form.
- Kommunikation page has 3 empty section headings — keep or fill?

## Deferred

- Full copy-polish pass over every text.
- Phase 3 workflow documentation.
- Phase 4 B2B case study: PDF handout + embeddable HTML.
