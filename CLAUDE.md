# Project: KIBH Website Rebuild (Case Study)

## Assignment (from Willy Li, Projektverantwortlicher — Bearbeiter: Hari)

**Goal:** Evaluate Claude Code as an alternative to WordPress for KI Beratung
Hessen (KIBH), and produce a B2B case study from the result.

**Background:** KIBH's current site runs on WordPress — market standard, but
with maintenance overhead, plugins, load times, hosting costs. This project
tests whether AI-assisted development (Claude Code) is a more modern,
efficient, economical alternative, using a real project as the test case.

### Phase 1 — Input & target picture
- Willy supplies new text/content requirements (see "New content" below)
- Design stays visually/stylistically close to the current KIBH site, content
  must be up to date

### Phase 2 — Build with Claude Code
- Build the site with Claude Code, based on the old design + new content
- Actively test: how well can Claude Code reuse/adapt existing design elements
  vs. how much has to be generated from scratch?
- Actively test: how easily/quickly can Claude Code make later small content
  or design changes? → time and note every such change, this is graded

### Phase 3 — Full documentation (very important)
Log from day 1, as you go:
- Starting setup — which tools/setup were used
- Workflow — actual interaction with Claude Code (prompts, iterations)
- Stumbling blocks — limits, bugs, unexpected effort
- Time spent — per step

### Phase 4 — B2B case study
Worked on closely with Willy (a case study is fundamentally a B2B sales
letter). Two output formats:
1. A polished handout PDF (slides) for client conversations/downloads
2. HTML/web content embeddable directly on the KIBH website
Core question it must answer: is switching to Claude Code economically
worthwhile, and what's the most efficient process for it?

### Success criteria
- Functional, modern, well-structured site in KIBH's familiar design, new content
- Transparent workflow report incl. pros/cons of Claude Code
- Finished, B2B-ready case study on the economics of the switch

### Payoff
If market-viable and profitable: foundation for a real web-migration service
offering, with a possible Werkstudent/side-job path for Hari.

## Design direction — NOT a 1:1 copy
- Keep the same fonts and overall visual language as kiberatunghessen.com
- Revise sections that feel too generic, add new sections where needed,
  correct/update texts
- Every such change is also a timed test case for Phase 3 — note how long it
  took and how it went

## Source reference
Live site: https://kiberatunghessen.com/ (WordPress + Elementor)

Current structure:
- Startseite: hero, client logos, "Warum wir?", 9 service/solution cards,
  3-step process, team bios (Willy Li, Ilya Volkov)
- E-Rechnung
- Ergebnisse (+ subpages: Potenzial Analyse, Kommunikation/Management,
  U2care, Automatische Rechnungsprüfung)
- Kontakt (consultation booking)
- Footer: Impressum, Vertraulichkeit (Datenschutz)

## New content
Willy's draft content for a new "Deep Reading Engine" (DRE) section/page →
see `docs/content-deep-reading-engine.md`. Three overlapping draft versions
exist there (structure/tone/one example differ) — confirm with Willy which
to use before publishing. Don't invent claims or numbers not in the drafts.

## Tech stack
- Static HTML/CSS/JS — no framework
- Deployment target: Vercel
- "Kostenloses Erstgespräch" (booking) flow: not yet decided — options are an
  embedded booking tool (e.g. Calendly) or a small contact form via a Vercel
  serverless function / form service. Don't build until decided.

## Assets
Logos/photos to be uploaded by Hari later. Use placeholders until then —
don't scrape/reuse images from the live site without asking.

## Git rules
- Never run `git push` or open a PR without asking first — every time, no exceptions
- Local commits are fine and encouraged (useful for the Phase 3 documentation trail)

## Open questions
- Booking/contact backend: not yet decided
- Final DRE section wording: pending Willy's sign-off