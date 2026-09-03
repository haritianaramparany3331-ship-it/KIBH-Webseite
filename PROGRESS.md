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

## 2026-09-02 — six micro-interactions

1. **Link underline reveal.** Hover wipes a 2px accent bar in from the left over 180ms, on inline body links and "read more"-type links: `.prose a`, `.case-body a`, `.booking__mail a`, `.site-footer li a`, `.case__more`, `.er-card__more`, `.member__link`, `.btn--ghost`. Nav links deliberately excluded — they already have their own hover pill.
2. Drawn as two stacked `background-image` bars, not an `::after`. An absolutely-positioned pseudo-element only underlines the first line box when a link wraps mid-paragraph, which happens in the legal pages' long sentences. `currentColor` on both bars means each context keeps its own colour — teal in body copy, lime in the footer — with no second rule.
3. Body-copy links keep a permanent 1px underline underneath (Hari's call, over dropping it) so they stay recognisable as links inside a block of text. `text-decoration: underline` removed from `.prose a` and `.case-body a`; the new block is the single source of truth.
4. `background-origin: content-box` was needed: `.btn--ghost` inherits 13px of vertical padding from `.btn`, which parked the bar that far below the text and read as a rule under the link, not an underline on it.
5. **Ergebnisse card hover** now matches the homepage testimonial cards exactly — `translateY(-3px)`, `--shadow-md`, accent border, same 180ms curve. Verified equal by computed style, not by eye.
6. Two things that had to change for it: the card gets `border: 1px solid transparent` so the border colour has something to animate (border-box, so it costs no size), and the hover has to be restated under `.page-ergebnisse` because that page's resting rule (0,2,0) outranks the base `.case:hover` (0,1,1) and would keep its own shadow throughout.
7. This is a deliberate departure from the WordPress original, which has no hover on those cards at all.
8. **Kontakt floating labels.** The four labels were `visually-hidden` with placeholders doing the visible work; they are now real visible labels that rise 15px and scale to 0.75 on focus or once the field has content. Same words, no copy change.
9. Placeholder is a single space so `:placeholder-shown` can tell empty from filled — that is what holds the label up after focus leaves, and it covers autofill. Label follows its input in the DOM so a sibling combinator reaches it; `for`/`id` still pair them.
10. Focus is a flat border-colour change and nothing else — no outline, no ring, no halo, per Hari. `--c-accent-dark` rather than `--c-accent` because the darker teal clears 3:1 against both the white field and the form ground; the label turning teal is the second half of the indicator.
11. **Magnetic booking CTAs.** Buttons pull 18 % of the cursor's offset from their centre, capped at 6px, within a 26px reactive margin, easing back on leave. Scoped to `a.btn[href="/kontakt/"], a.er-btn[href="/kontakt/"]` — 10 buttons. Excluded on Hari's call: the homepage full-width CTA band and the Kontakt page's "Termin Buchen" tab.
12. JS sets `--mag-x`/`--mag-y`; CSS composes them with the button's existing 1px hover lift. Writing `transform` inline would have overwritten that lift. `.btn.is-magnet` (0,2,0) is needed to beat `.btn:hover` (0,1,1).
13. The rect a transformed button reports is the displaced one, so the applied offset is subtracted before measuring — without it the button chases its own transform. Also recomputed on scroll, since scrolling moves buttons past a stationary cursor.
14. **Logo strip → marquee.** JS moves the 7 logos into a flex track, clones the group `aria-hidden`, and slides exactly one group width per cycle, so the loop has no seam. 42 px/s, duration derived from the measured group width (1176px → 28s) so speed is constant at any viewport. Pauses on hover. Edge mask so logos enter and leave rather than being cut off.
15. Defect found by `wt_site.py`: at 390px the last two logos never loaded. `loading="lazy"` defers images parked hundreds of pixels off to the right of the track, and they would have popped in blank as the marquee brought them round. JS now sets `loading = "eager"` when it upgrades the strip — 113 KB for all seven. Lazy loading stays in the no-JS fallback.
16. `tests/qa.py` needed a marquee exemption: the track is deliberately wider than its box, with `overflow: hidden` doing the clipping. Over-wide is the mechanism, not a defect.
17. **Cursor-following glow.** A 44rem radial in `--c-accent` (#76abae, the testimonial quote-panel teal), trailing the cursor at 7.5 % of the remaining distance per frame. rAF loop stops once it catches up, so an idle page schedules no frames. `--glow-a` in the tokens block is the single dial for strength.
18. First version was one fixed copy at `z-index: -1`. Hari could not see it, and measurement said why: at that depth any opaque section ground hides it. It showed over 41 % of the site and **0 % of `/ergebnisse/` and `/deep-reading-engine/`**, where every section paints its own ground — and the homepage hero swallowed the whole first screen.
19. Fixed by giving each ground-painting `main > *` (and the footer) its own clipped copy, inserted by JS: the section is made a stacking context with `isolation: isolate`, and the copy sits at `z-index: -1` inside it. Paint order there is the section's own background, then the glow, then everything the section contains — so it lies on the ground and still passes under every card, heading, image and paragraph. 3–5 grounds per page. Strength raised 0.16 → 0.26 at the same time.
20. Now visible on every page: centre delta 34–44/255, and the lit area is 20–28 % of the viewport, which is the glow's whole geometric footprint. `/ergebnisse/` 0 % → 16.7 %, `/deep-reading-engine/` 0 % → 25 %. Cards and the booking box correctly still sit on top of it.
21. Proven not to move anything: full-page screenshots of 12 pages × 2 viewports before and after, with every glow element stripped, are pixel-identical on 23 of 24. The 24th is `/kontakt/`, where two runs of the *same* build differ more (398 px) than before-vs-after (199 px), in the same 30×25 box where the typewriter caret blinks.
22. Frame cost with the cursor moving: median 16 ms, p95 22–24 ms, on all four heaviest pages.
23. All six honour `prefers-reduced-motion`; the three JS ones also bail on coarse pointers except the marquee, which is the point on touch.
24. `tests/qa.py` green (11 pages × 5 viewports). `scratchpad/u2/wt_site.py` green (12 pages × 5 viewports). Zero console errors. Scripts in `scratchpad/micro/`: `verify.py` (all six, computed-style assertions), `glow.py` (pixel deltas, own PNG decoder), `coverage.py` (what fraction of each page can show the glow), `zoom.py`/`crops.py` (3× crops), `before.py`/`after.py` (pixel-identity proof), `glow2.py` (visibility by pixel diff), `perf.py` (frame cost).
25. Commits `ae99db8` (the six interactions) and `e2c56c7` (the glow fix). Pushed to `origin/main` on Hari's go-ahead.

## 2026-09-03 — mobile/tablet responsive audit and fix pass

1. **Method.** 12 pages × 6 viewports, every context emulated as a touch device
   (`is_mobile`, `has_touch`), which is what makes `hover: none` /
   `pointer: coarse` report correctly: 360×740 and 414×896 portrait, 640×360 and
   896×414 landscape, 768×1024 tablet portrait, 1024×768 tablet landscape.
   Scripts in `scratchpad/resp/`.
2. **The structure was already sound.** Zero horizontal page overflow, zero
   elements past the viewport edge, zero clipped text boxes, zero headings
   escaping their container — at every one of those 72 combinations, before any
   fix. The audit groups findings by defect rather than by page, so one CSS bug
   reads as one line: 35 distinct at the start, 3 at the end, all three
   deliberate.
3. **Hero compound chopped below 390px.** `--fs-hero` was pinned at 40px, where
   "maßgeschneiderte" is 356px wide; at 360px the column is 328px, so it broke
   mid-word with no hyphen (`hyphens: manual` is on for display headings). Now
   `clamp(2rem, calc((100vw - 2rem) / 9.1), 2.5rem)` — the word is about 8.9×
   the font size wide, so dividing the column by 9.1 keeps it whole with room to
   spare. Verified fitting from 320px up.
4. **Eyebrow glyph floated to the middle of the block** once the label wrapped
   to two lines on a phone. `align-self: flex-start` plus a 0.28em offset marks
   the first line instead.
5. **Body text 15px → 16px on phones.** Running text should not get smaller on
   the screen held closest to the face, and 16px is also the threshold under
   which iOS Safari zooms the page when a field takes focus.
6. **Form fields pinned to 16px** independently of `--fs-body`, so that
   threshold can never be crossed by a later token change. Every field and
   button on Kontakt now clears 16px and 44px at every width.
7. **Touch targets.** Footer links were 18px tall on every page — the `gap`
   carried the rhythm while each link was only its own line box. They now carry
   `padding-block` and the gap shrinks to match, so the pitch is unchanged and
   the targets are 31px. Same for "Mehr Lesen" on Ergebnisse (18 → 32px) and the
   contact address on the Impressum, which is a whole paragraph rather than a
   word in a sentence and so is a target in its own right. Links inside running
   text are deliberately left alone: WCAG 2.2 exempts them, and making them
   `inline-block` would stop a long URL wrapping.
8. **`.section--tight` was looser than a normal section on mobile** — normal
   sections scale 80 → 56px through `--sp-9`, but tight ones sat on `--sp-8` at
   64px at every width. Scaled so the order holds.
9. **Legal-page headings.** `.prose h2` at 32px ran to seven lines in a 328px
   column and pushed the section it introduces off screen. 26px on phones, with
   the 64px top margin scaled to 48px.
10. **Landscape phones** had a 76px sticky header eating a fifth of a 360px-tall
    viewport, and desktop-height section padding in a viewport with almost no
    vertical room. Under `(orientation: landscape) and (max-height: 500px)` the
    header is 56px and sections scale down.
11. **Orphaned words.** `text-wrap: balance` on every heading and
    `text-wrap: pretty` on prose took 13 headings ending on a lone short word
    down to 1. The survivor is `/ergebnisse/` h1 at 414px, where
    "Umsatzpotenziale" is 305px wide in a 382px column — balance is applied and
    this is its own best answer. Not fixable without touching the text.
12. **Hover effects can latch on touch.** A touch browser applies `:hover` on
    tap and iOS keeps it applied until the visitor taps elsewhere. Ten
    decorative rules are now inside `@media (hover: hover)`: the three card
    lifts, the homepage solution card's full teal fill, the DRE pillar and case
    tiles, the button lift, and the link underline reveal. Keyboard
    `:focus-visible` keeps the underline in all cases. Verified both ways —
    every one fires with a mouse, none fires under touch emulation.
13. **The logo marquee froze permanently on the first tap.** Pausing was a
    `:hover` rule, so a latched hover stopped it for good. It is now a class the
    script toggles from pointer events: `pointerenter`/`leave` for a mouse,
    `pointerdown`/`up` for a finger. That also gives a touch visitor
    press-and-hold, the only way they had to stop it at all (WCAG 2.2.2).
14. **Checked and found correct, no change needed:** viewport meta; the drawer
    at every width (all 10 links reachable, scrolls internally where the screen
    is short, closes again); the magnetic CTAs and cursor glow, which already
    bail on coarse pointers and create nothing at all; `prefers-reduced-motion`,
    under which the marquee is never upgraded, no glow or magnet exists, and no
    element is animating.
15. **One audit false positive, corrected in the checker:**
    `.case-quote__logo` reported as distorted at every width. Its content box is
    3.012 against a natural 3.012 — the padded chip around it inflates only the
    border box. The image aspect check now measures the content box.
16. **Left deliberately:** the 12px `.eyebrow`, which is a tracked uppercase
    label rather than running text; and the 7px "BE Renovierung" wordmark, which
    is Hari's own call (see 2026-08-30, item 14).
17. `tests/qa.py` green, `scratchpad/u2/wt_site.py` green, all six
    micro-interactions still verified with a mouse, zero console errors.
18. Scripts, all re-runnable against the dev server: `scratchpad/resp/audit.py`
    (the 12 × 6 sweep, grouped by defect), `behave.py` (nav, touch behaviour,
    reduced motion), `nav_form.py` and `nav2.py` (drawer reachability, form,
    layout metrics per breakpoint), `hovergate.py` (every gated hover, mouse
    vs touch), `hold.py` (marquee press-and-hold), `hero.py` (the compound
    word against its column at each width), `shot.py` (phone screenshots).
19. Commit `709e5ed`. Pushed to `origin/main` on Hari's go-ahead.

## 2026-09-03 — the closed nav drawer was stealing taps

1. **Symptom Hari reported:** on a phone, tapping "Vertraulichkeit" in the
   footer sometimes landed on the right page and sometimes on the wrong one.
2. **Not the hrefs.** All 44 distinct links across the 12 pages were audited
   label-against-target: every one points where its label promises and every
   internal target returns 200. Intermittence was the clue — a wrong `href` is
   wrong every time.
3. **Cause.** `.nav` is the mobile drawer: `position: fixed`, and when closed
   `opacity: 0` and `visibility: hidden`. The drawer's own rule for the
   Ergebnisse submenu set `visibility: visible`, to undo the desktop rule that
   hides it until its parent is hovered. But visibility is inherited, and a
   child may override an ancestor's `hidden` with its own `visible` — so the
   four sub-links stayed hit-testable while the drawer was shut. Invisible,
   because opacity is not overridable that way, but occupying a fixed 326×192
   band at y 338–530 on a 390px phone and swallowing every tap in it.
4. That band is fixed to the viewport, so which control it stole depended on
   the scroll position — hence "sometimes". It affected every page, not just
   the footer, and sent the visitor to an Ergebnisse subpage.
5. **Fix.** `visibility: inherit` on the drawer's submenu, so it is visible
   exactly when the drawer is. Plus `pointer-events: none` on the closed
   drawer and `auto` when open, which does not depend on inheritance reaching
   every descendant — a fully transparent element still takes taps, so opacity
   alone would never have been enough.
6. **Verified.** Every link and button on all 12 pages, at 360, 414, 640×360
   and 768 wide, scrolled the full page height in viewport-sized steps: 0
   mis-hitting controls, from 4 distinct before. Drawer still opens, all 10
   links reachable at every width, closes again.
7. Two audit false positives found and corrected in the tooling while chasing
   this: the bounding-box centre of an inline link that wraps falls in the
   gutter beside its shorter second line, so the probe now tests each line
   fragment; and `scrollIntoView` is animated here (`scroll-behavior: smooth`),
   so measuring synchronously after it reads pre-scroll coordinates.
8. Not a defect: at 360px, scrolled fully to the bottom, the footer wordmark's
   upper half sits under the sticky header. Its lower half is tappable and
   "Startseite" directly below it goes to the same place.
9. `tests/qa.py` green, `scratchpad/u2/wt_site.py` green. Scripts:
   `scratchpad/resp/links.py` (label vs target vs HTTP status),
   `taps.py` (every control, every page, hit-tested), `phantom.py` (the
   diagnosis), `nav2.py` (drawer reachability by stepped scroll).

## 2026-09-03 — defect pass: only the consistency fixes kept

Hari asked what is missing for the site to read like a €10 000 website, and set
the terms: fix what is objectively broken, keep the look. Hero image and the
Kontakt page out of scope. Three stages were built and shown, each as its own
commit; he kept one.

1. **Kept — one component, one appearance.** The homepage solution-card title
   rendered at 24/20/18px depending on the card, because Elementor sized the two
   longest ones down so they would not swamp the box. Six cards in two rows
   therefore read as six different components. One size now; the long titles
   wrap, which is what the line-height is for.
2. The "Mehr" toggle used a literal `>` character where every other link on the
   page uses the shared chevron SVG. It carries that chevron now, turned to
   point down and flipped when the extra cards are open. The label moved into
   its own `.btn__label` span so the disclosure script can swap the words
   without discarding the chevron.
3. "Kernpunkte der Lösung" on U2care was a `<p>` at 28px weight 400 — a heading
   rendered as body text and missing from the document outline. It is an `<h3>`
   now and the outline reads H1 H2 H2 H3 H2.
4. **Rejected — reading measure.** Body copy ran 131–144 characters a line on
   the case pages and 109 on the legal pages, against a comfortable 60–75. A cap
   on the text elements alone brought them to 71–73 and left headings, figures
   and card grids at full width. Hari: "Stage 1 and 2 are bad." Reverted.
5. **Rejected — contrast.** Five measured failures on light grounds, including
   the closing call to action at 1.37:1 (lime on the #f2f3f2 band) and
   "Linkedin" and "Mehr Lesen" at 2.56:1. Fixed with teal tokens the palette
   already had. Reverted.
6. **Rejected — the focus ring.** `:focus-visible` is `3px solid var(--c-accent)`
   and the primary button's background is that same #76abae, so on that button
   the ring measures 1.0:1 and reads only as the 3px offset gap. A two-tone
   white-and-dark ring that cleared 4.74:1 there and 12.14:1 on the dark footer
   was built and turned down. His words: "let it be blue greeny like that, it's
   better than black even though it is the same color as the button, the user
   can still see the focus." Left as it was; recorded here so it is not raised
   again.
7. None of the three had been pushed, so the rejected ones were rewound rather
   than reverted and the branch carries only the kept work — no revert commits
   in the history. They remain in the reflog for about 90 days if any part is
   wanted after all: `75564d5` measure, `6004882` contrast, `3f427be` the full
   stage 3 including the two-tone focus ring.
8. `tests/qa.py` green, `scratchpad/u2/wt_site.py` green, responsive audit
   unchanged at its 3 known findings, zero console errors.
9. Commit `fd1483a`. Pushed to `origin/main` on Hari's go-ahead.

## Still missing, in my view — recorded, not acted on

Hari asked the question and then put the first two out of scope. Worth
revisiting rather than losing.

- **The Kontakt page.** Every CTA on the site points at a page whose main panel
  is a dashed, hatched wireframe, with the secondary tab greyed so it reads as
  disabled. Nothing else costs as much credibility. Making the placeholder look
  finished needs no backend and does not pre-empt Willy's decision.
- **A point of view.** The hero is a stock gold Rodin-thinker robot, the image
  most AI consultancies use, while the genuinely distinctive assets — real
  client names, real numbers, the zig-zag process diagram — are presented as
  ordinary cards.
- **The third typeface.** Plus Jakarta Sans on E-Rechnung and the four case
  pages against Verdana + Mulish everywhere else; the site reads as two sites.
- **Page weight.** `assets/img` is 6.6 MB, E-Rechnung alone 3.8 MB. WebP at
  display size changes no pixel a visitor sees, and would restore the "24×
  lighter than WordPress" figure in `docs/performance-baseline.md`, stale by
  more than an order of magnitude and a headline number for the Phase 4 case
  study.

## 2026-09-03 — images to WebP, and the case-study number corrected

Hari asked what "hero, third typeface and page weight" meant. Answering the
third one turned up the serious item: `docs/performance-baseline.md` claimed the
rebuild was **24.4x lighter than WordPress**, measured back when every image was
a placeholder and the image row read 0 KB. With the real assets in, the homepage
was 2 221 KB against WordPress's 2 464 KB — about **1.1x**. The headline number
of the case study this whole project exists to produce was wrong by a factor of
twenty.

1. `assets/img` is **908 KB, from 6.6 MB**. 24 files re-encoded to WebP at the
   size they are actually displayed: largest rendered size across 1440/768/390,
   doubled for retina, never upscaled past the source.
2. Two quality settings. Photographs at 0.82; flat graphics that carry lettering
   — the certificate, the TÜV mark, the client logos and wordmarks — at 0.94,
   because lossy WebP softens hard edges and small type first. Checked by eye at
   display size before committing to it: indistinguishable.
3. Per page, fully scrolled: `/` 2 221 → **740 KB**, `/e-rechnung/` 4 075 →
   **459 KB**, `/ergebnisse/` 1 005 → **258 KB**, ARP 795 → **255 KB**.
4. `tools/encode-webp.py` adds **no build dependency** — `package.json` still has
   none, which is itself part of what the case study argues. There is no sharp,
   no PIL and no ImageMagick on this machine; Chromium ships a WebP encoder and
   Playwright is already here for the suites, so the script draws each source
   into a canvas at the target size and calls `canvas.toDataURL('image/webp', q)`.
   Alpha survives, so the cut-out logos and round avatars keep their transparency.
5. It lives in `tools/` rather than the scratchpad on purpose: it is the evidence
   for the Phase 3 write-up of how this was done without a toolchain.
6. **`tests/compare.py` was measuring dishonestly** and now measures twice. It
   only captured the load event, and both sites lazy-load their images, so the
   comparison counted almost none of WordPress's. It now also scrolls to the
   bottom on both sides.
7. Honest figures, 2026-09-03: **5.1x lighter on load** (2 464 KB vs 481 KB) and
   **3.7x fully read** (2 735 KB vs 740 KB). The stylesheet is where the
   difference really sits — Elementor's single combined sheet is 1 363 KB against
   126 KB here.
8. **Images are the one line WordPress still wins**, 365 KB to our 531 KB. It
   serves `srcset` variants sized to the viewport where we serve one file, and
   `hero-robot.png` is 216 KB of our 531 — the only raster left in its original
   format, untouched at Hari's request. Its WebP would be roughly 30–40 KB,
   which would put us at ~560 KB fully read (**4.9x**) and below WordPress on
   images too. Flagged, not done.
9. `docs/performance-baseline.md` rewritten end to end: both measurements, the
   resource breakdown, the per-page table, how the encoding was done, and a
   caveats section saying plainly that the old 24.4x was never true of the
   finished site and must not be reused. Timings are deliberately not quoted —
   localhost against the public internet is not a fair comparison, and that has
   to wait for the Vercel deploy.
10. Proven to move nothing: full-page screenshots of all 12 pages at 1440 and 390
    before and after are identical in height except **one pixel** on
    `/e-rechnung/` at 390px. That came from correcting `width`/`height`
    attributes that had never matched their files — `image-1` was declared
    399×499 for a 640×800 image — so it removes a layout shift rather than
    adding one. Pages with no images are pixel-identical.
11. `tests/qa.py`, `scratchpad/u2/wt_site.py` and the responsive audit all green;
    CLS unchanged; no console errors. The one page reading CLS 0.05 is
    `/ergebnisse/automatische-rechnungspruefung/`, and the shift sources are the
    nav and body text, not any image — it is the web font swapping in, which
    predates this work.
12. Commit `e766fea`. **Not** pushed.
13. **Next, not yet started:** unify on Verdana + Mulish and drop Plus Jakarta
    Sans, which Hari chose after I explained that the third typeface is not our
    mistake — the live WordPress site uses it on E-Rechnung and the four case
    pages, and our rebuild copied that faithfully. That stage changes how five
    pages look and is committed separately so it can be dropped on its own.

## Open — waiting on Hari

- **Glow strength.** `--glow-a` in the tokens block of `assets/css/main.css` is the one dial: 0.26 now, 0.15 is roughly where Hari could not see it, 0.35 starts to read as a spot rather than a warmth. Say a direction and it moves.
- **The logo marquee's only touch pause is press-and-hold.** Added 2026-09-03 alongside the hover pause. `prefers-reduced-motion` still turns it off entirely. WCAG 2.2.2 wants a mechanism a visitor can find, and a hold gesture is not discoverable — a visible pause button would be, but it is new UI the original does not have, so it was not added unasked.
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
