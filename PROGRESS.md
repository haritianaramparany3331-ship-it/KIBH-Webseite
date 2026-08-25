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

## 2026-08-25 — housekeeping

1. `PROGRESS.md` created. Commit `869b284`.

## Open — waiting on Hari

- Real assets: logos, team photos, client logos. Placeholders until then.
- Vercel deploy. Last known failure: Root Directory set to `src/pages`, so Vercel looked for `src/pages/dist`. Fix is to blank it and clear the dashboard Build/Output overrides. Outcome not confirmed.
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
