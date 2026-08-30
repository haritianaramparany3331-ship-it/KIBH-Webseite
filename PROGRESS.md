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
12. Two spelling corrections on Hari's instruction, the only place our text departs from the original: it splits both verbs, German writes them closed up — "dich kennen zu lernen." → "dich kennenzulernen.", "zusammen zu arbeiten." → "zusammenzuarbeiten.".
13. The caret trails the last typed letter. The width of the longest phrase is reserved on the wrapper rather than on the text node, so the caret stays inline 1px behind the text while the slack sits to its right and nothing reflows.
14. `scratchpad/verify_kontakt.py`: 5 viewports, tab switching both ways, strip position per breakpoint, keyboard arrows, hover, field geometry, submit does not navigate, headline actually types, and a six-way text diff against the live page. Green. Full QA suite green.
15. Pushed together with the homepage, Ergebnisse and legal-page work — 11 commits, `39e2118..ddf82a2`. Live, `main.f22ba310.css`.

## 2026-08-30 — case-study pages unified on U2care, nav bold

1. Hari's call: the four pages under `/ergebnisse/` all take the **U2care** original's design, overriding each page's own styling. Text stays 1:1 with each page's *own* original. Commits `5ca9b9c`, `d40edd7`.
2. Design system extracted from the live U2care page by measurement, not by eye → `.page-case` in `main.css`. Plus Jakarta Sans, 18/24 body, 1140 content column, H2 48/600 in `#76abae` with a 4px rule 10px under it, cards 367 wide with a 1px teal border and a 20px radius, centred 16px text over a 50px grey icon, 20px between blocks, everything fading up on scroll.
3. Container widened by the gutter (`calc(--container + 2 * --sp-5)`) so the content column measures 1140 like the original and the cards land on 367, not 351.
4. Hero: black + teal bloom borrowed from Ergebnisse/DRE, lime "Case study" line, white headline, client quote inside the band. The original's hero is a licensed photograph — Hari chose the CSS ground over downloading it.
5. Headline is 52px, not the original's 64px: three of the four titles are twice the length of U2care's and filled the screen at 64.
6. Card icons drawn as inline line-art SVG (user-check, invoice, gears, user-cog, rocket) — the original uses an icon font we do not ship. Numbered pages keep their `1/2/3` badge in the same slot.
7. **Text drift found and closed.** The live pages had moved on since the Stage 2 rebuild:
   - Kommunikation gained *Erkenntniss*, *Lösung* and *Probleme* with their numbered cards — the three sections that were empty when we first built it.
   - Automatische Rechnungsprüfung gained the full *Ergebnis* paragraph and the "Mehr Qualität. Mehr Transparenz. Weniger Aufwand." band.
   - Potenzial Analyse gained the real step titles, their lead-ins and the "Am Ende erhalten Sie…" paragraph.
   - U2care gained "Kernpunkte der Lösung" and three result cards in place of a tick list.
8. Closing "Termin buchen" bands removed from all four — no live original has one, they were ours.
9. Grammar-only corrections, nothing else touched: "E-Rechung" → "E-Rechnung"; "Wiederstände Identifizieren" → "Widerstände identifizieren"; a missing space after a full stop on Kommunikation and on Automatische Rechnungsprüfung; six missing terminal full stops on U2care.
10. Fixed: the shared `.ticks` lays each item out as a flex row, so a leading `<strong>` became its own flex item — "Handlungsempfehlung" broke across two lines and the colon was pushed off it. Hanging indent instead.
11. Fixed: Potenzial Analyse's step lists are centred on the original, leaving the bullets at ragged positions. Cards holding a list are set left.
12. **Nav** (separate ask). The original sets it in Avenir 600, and Avenir ships 400/700 only, so it renders bold; Mulish has a real 600, so ours came out semibold and read greyer than the headings next to it. Now 700, 15 → 16px. Dropdown 500 → 600.
13. Fixed: the nav drawer opened at 1025px but the row has never fitted there — it needs 1120px. Between 1025 and 1071px the CTA pushed **every page** into horizontal scroll. Breakpoint moved to 1119px, in CSS and in the `matchMedia` that resets it.
14. Fixed: the homepage loaded with ~40px of horizontal scroll under 1300px. Its nine `data-anim="right"` blocks sit 64px right until revealed; DRE and E-Rechnung already had `overflow-x: clip` on `<main>`, the homepage never did.
15. `scratchpad/u2/verify_case.py` — design values, word-level text diff against each live original, overflow at 5 viewports. Green. `scratchpad/u2/sweep.py` — 12 pages × 8 viewports, on load and settled, 0 horizontal overflow. `scratchpad/u2/wt.py` — webapp-testing pass, 4 pages × 5 viewports: no console errors, no failed requests, no clipped text, no card collisions, even card heights, heading order intact, every reveal fires, every link resolves and focuses. `tests/qa.py` green.
16. **Not** pushed yet — waiting on Hari.

## 2026-08-30 — real photos and logos placed site-wide

1. Hari uploaded the real imagery into `assets/img`, organised by section. Commits `b395903`, `27d9e8c`.
2. **Assets normalised.** The upload arrived with mixed-case folders, spaces, umlauts and parentheses, five images duplicated across up to seven folders, and `erechnung/` case-renamed to `ERechnung/` — the same directory on Windows, a different one on Vercel's Linux, which would have 404'd every E-Rechnung image in production. Now 21 unique files on lowercase ASCII paths: `kibh-logo.png`, `erechnung/`, `startseite/` (+ `logos/1..7`), `ergebnisse/`.
3. `bg-1.png`, `graphic.svg` and `ss.svg` restored — the re-upload dropped them and the E-Rechnung page still needs them.
4. **Mistake, and the recovery.** The normalisation script deleted the files it had just moved: on Windows `makedirs("startseite")` reuses the existing `Startseite`, so a lowercase `startswith` guard missed them and they were counted as duplicates. They were untracked, so git could not restore them. All 21 were re-fetched from their sources — the live site plus the seven strip logos already pulled into the scratchpad — and every one came back at the same dimensions and byte size Hari uploaded; the five with recorded hashes match exactly. Committed immediately so it cannot recur.
5. Every placement matched by looking at the file and then checking how the live page displays it, not by filename.
6. Placed: header + E-Rechnung CTA wordmark; homepage hero robot; all 7 client logos in the live site's own order; 3 homepage testimonial portraits; the AI-Consultant certificate and the TÜV Rheinland mark; Willy and Ilya; 7 of the 11 Ergebnisse cards; the hero portraits on U2care, Kommunikation and Potenzial Analyse; the Hinnerbäcker wordmark on the two Hinnerbäcker case studies; the Bauwesen photo on Automatische Rechnungsprüfung.
7. Torsten's small round avatars use the square 1024×1024 crop, not the wide 1024×984 — same shot, but at 57px the wide one is mostly shirt. The live site squashes the wide file to 57×55.
8. The Hinnerbäcker wordmark is a JPEG with its own white ground; the original sits it on a light band, ours is a dark hero, so it gets padding and a radius and reads as a chip.
9. Strip logos: 300×300 files with ~25 % blank margin baked in, so a 7rem box brings the marks to ~84px. `transform: scale()` was tried first and dropped — it grows the box as well as the paint, and the outer logos then reported as overflowing.
10. Team portraits stay round: the files are circular cut-outs on white, so a round mask lands on the circle. The original's contain-in-a-rectangle leaves white bars.
11. `scratchpad/u2/wt_site.py` — webapp-testing pass, 12 pages × 5 viewports: every image loads, none stretched, squashed, upscaled past its own resolution or missing an alt; no overflow, no console errors, no failed requests. 0 problems. Overflow sweep and `tests/qa.py` green.
12. **Not** pushed yet — waiting on Hari.

## Open — waiting on Hari

- **Page weight.** With the real images in, the homepage is 2 189 KB and E-Rechnung 4 044 KB, against the 101 KB measured in `docs/performance-baseline.md`. The comparison there no longer holds — the biggest single files are `zertifikat-ai-consultant.png` (1 184 KB) and the four E-Rechnung PNGs (3 053 KB together). Re-encoding to WebP at display size would win most of it back; not done unasked because it changes the uploaded assets.
- `ergebnisse/torsten-krueger.jpg` (the wide crop) is now unused — the square one reads better at avatar size. Kept in case it is wanted somewhere.
- The logo's "HESSEN" line is drawn in a light grey meant for a white ground, so it goes faint on the dark footer. A light-on-dark variant of the file would fix it; not filtered in CSS because that shifts the brand colour.
- The 🙂 inside Martin Kraus's quoted testimonial on `/ergebnisse/`. Left in — it is a customer's own words.
- The Kontakt form is silent when submitted: `data-inert` stops it navigating, but nothing tells the visitor it is not connected yet. A note there would be text the original does not have, so it was left out — say if it should be added.
- The live Martin Kraus card on `/ergebnisse/` carries a heading, "Rechnungsverarbeitung"; ours has none. Adding it is copy, so it was left alone.
- The teal section headings on the four case-study pages sit at 2.56:1 against white, under the 3:1 WCAG needs for large text. That colour is the U2care original's and Hari asked for it, so it was not changed. `--c-accent-dark` (#5f9295) would clear it at ~3.6:1 if he wants.
13. Entropia and Business Elegance wordmarks added afterwards, commits `7040b1d`, `8323f08`. Both are wide lockups rather than square marks. A stacked chip above the attribution was built first, then dropped on Hari's call: all ten slots use the same 57px circle as the photo avatars, with the wordmarks contained inside (Entropia lands at 43×15, Business Elegance at 43×36). Small on purpose — the company name is spelled out beside the circle, so the mark only holds the place.
14. BE Renovierung has no logo; per Hari its circle carries the name as type, at the 7px that fits "Renovierung" across a 57px circle unbroken.
15. CSS trap worth remembering: an `auto` grid row sizes to its own content, so a percentage height cap on an image inside it is circular and the image simply overflows. The circle is a fixed-size flex container for that reason.
16. Footer wordmark, commit `875dc5e`. It was still carrying the stand-in — a teal 84px square reading "KIBH" beside the name in type. Now the same logo file as the header at 60px, with the lime tagline under it; the "KI Beratung Hessen" line is gone because the logo says it. That was the last use of the stand-in, so `.brand__mark`, `.brand__text`, `.brand__name` and their three footer overrides were deleted rather than left as dead rules.
17. **Every placeholder on the site is now a real asset.**
18. Browser-tab icon, same as the original: the teal robot-head-over-KI mark. Was a hand-drawn stand-in SVG. The three PNGs WordPress serves (32, 192, 180) are copied in byte-identical and linked the same way the live head links them; `favicon.svg` deleted. The 270×270 `msapplication-TileImage` was skipped — Windows 8/10 start-tile pinning, dead tech, 22 KB.
19. Verification trap: headless Chromium never requests a favicon at all — no tab UI to draw it in. The first check reported all 12 pages broken. Confirmed against the live WordPress site, which behaves identically headless. `scratchpad/u2/favcheck.py` runs headed for that reason; 12/12 pages fetch `favicon-32.png`, no `/favicon.ico` fallback, no failed requests.

## Open — waiting on Willy

- Booking backend for "Kostenloses Erstgespräch": Calendly embed vs. serverless form.

## Deferred

- Full copy-polish pass over every text.
- Phase 3 workflow documentation.
- Phase 4 B2B case study: PDF handout + embeddable HTML.
