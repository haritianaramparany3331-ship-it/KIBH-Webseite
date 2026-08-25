# PROGRESS

Session log for Claude. Read this first. Update it at the end of every session.
Newest stage at the bottom. Keep entries short.

## Setup

- Static site, no framework. `build.js` reads `src/pages/*.html` + `src/partials/`, writes `dist/`.
- Pages carry a JSON front-matter comment: `<!--{ "title", "description", "url" }-->`.
- `npm run dev` = build + local server on `http://localhost:4173`.
- Deploy target: Vercel. Repo: `haritianaramparany3331-ship-it/KIBH-Webseite`, branch `main`.
- `vercel.json` holds build config, `cleanUrls`, `trailingSlash`, and the `/index.php/*` redirects from the old WordPress URLs.
- QA: `python tests/qa.py` (Playwright). 11 pages x 5 viewports. Checks links, console errors, box overflow, and word-fit.
- Run Python through the Bash tool, not PowerShell — `python.exe` is not on the PowerShell PATH.

## Stage 1 — foundations (done)

1. `git init`, `.gitignore`, directory structure, `CLAUDE.md`.
2. Design system extracted from the live Elementor kit into CSS custom properties → `docs/design-system.md`.
3. Old URL structure mapped → `docs/url-map.md`.
4. Content inventory of the live site + list of its defects → `docs/content-inventory.md`.
5. Willy's raw DRE drafts stored → `docs/content-deep-reading-engine.md`.

## Stage 2 — 1:1 rebuild (done)

1. All 10 pages rebuilt faithfully: Startseite, E-Rechnung, Ergebnisse + 4 subpages, Kontakt, Impressum, Vertraulichkeit, plus a 404.
2. Shared header/footer partials, `assets/css/main.css`, `assets/js/main.js`.
3. Placeholder images throughout — real logos and team photos still pending from Hari.
4. QA suite written and green.
5. Performance measured vs. the live WordPress site → `docs/performance-baseline.md`. Static build is 24x lighter (101 KB vs 2 464 KB).

## Stage 3 — Deep Reading Engine (done)

1. New page `/deep-reading-engine/`, built from Willy's three overlapping drafts merged and polished.
2. Reuses only existing components — no new design language.
3. Entry points added: nav, footer, and a dark teaser band on the homepage.
4. Nav drawer breakpoint moved 900px → 1024px. The 5th nav item was pushing the CTA off-screen.

## Stage 3b — cleanup pass (done)

1. All 18 emoji card icons removed site-wide. `.card__icon` CSS deleted.
2. 16 German text-fitting defects fixed (hero clamp, `blockquote` UA margin, `.grid--4` column counts, `.pillar` padding, hyphenation limits).
3. `audit_wordfit()` added to `tests/qa.py` so this class of bug is caught automatically from now on.
4. Two `laptop`/`tablet-sm` viewports added to QA — the old 390/900/1440 set had a blind spot.

## Open — needs Hari

- Real assets: logos, team photos, client logos.
- Vercel: last known failure was Root Directory set to `src/pages`. Fix is to blank it and clear the dashboard Build/Output overrides. Outcome not confirmed.
- The 🙂 inside Martin Kraus's quoted testimonial on `/ergebnisse/`. Left in — it is a customer's own words, so removing it is a content call.

## Open — needs Willy

- Which DRE draft framing is authoritative.
- Draft 3's third use case cuts off mid-sentence after "Angebot".
- Booking backend for "Kostenloses Erstgespräch": Calendly embed vs. serverless form. Do not build until decided.
- Kommunikation page has 3 empty section headings — keep or fill?
- Impressum was translated to German. Live site had it half in English. Confirm or revert.

## Deferred by Hari

- Full copy-polish pass over every text ("get rid of the AI slop"). Its own separate piece of work. Do not pre-empt it by rewriting copy during other tasks.
- Phase 3 workflow documentation.
- Phase 4 B2B case study (PDF handout + embeddable HTML).

## Rules that bit us before

- Never `git push` or open a PR without asking. Every time.
- Fix rendering/coding defects anywhere without asking. Never change content logic, wording, or structure.
- No emoji as UI elements.
- Work in stages. Commit, then stop and wait for approval before the next one.
- Commits need the `Co-Authored-By` and `Claude-Session` trailers.
