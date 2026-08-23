# KIBH Website — Build Plan

## Context

KI Beratung Hessen runs on WordPress + Elementor. We're rebuilding it as a
static HTML/CSS/JS site — faster, cheaper to host, and with no plugin
surface to maintain.

Three stages, executed in order:

1. **Foundations** — project setup, content inventory, design system
2. **1:1 rebuild** — faithful reproduction of the current site → **commit, then stop**
3. **Changes** — text revisions, new sections, new features — *only after explicit approval*

**Stage 3 does not begin until you approve it.** Everything the brief calls
for that isn't a faithful copy — rewriting generic sections, the Deep
Reading Engine, the booking flow — lives in Stage 3. Stage 2 is a replica
and nothing more.

Workflow documentation, time tracking, and the B2B case study from
`CLAUDE.md` are out of scope here and handled separately afterwards.

---

## Scope

`/e-rechnung/` and `/kontakt/` both return 404 on the live site, so the real
URL structure differs from what `CLAUDE.md` assumes. Those sections stay
unbuilt pending Willy's clarification, and keep returning 404.

| Page | Stage |
|---|---|
| Shared layout — header, nav, footer, CSS | 2 |
| Startseite | 2 |
| Impressum, Datenschutz | 2 |
| Custom 404 | 2 |
| E-Rechnung | Deferred → 404, pending Willy |
| Ergebnisse + 4 subpages | Deferred → 404, pending Willy |
| Kontakt / booking | Deferred → 404, pending Willy |
| Deep Reading Engine | 3 |
| Generic-copy rewrites, new sections | 3 |

The nav still lists the deferred sections, so those links hit the 404 page.
It's styled to match the site, so it reads as "not ready" rather than
broken.

---

## Stage 1 — Foundations

**1.1 Project setup**
Node.js and Git are already installed. `git init` locally, `.gitignore`,
directory structure. Local commits only — no remote yet. You'll send the
GitHub repo URL later and I'll wire up the remote and Vercel then; until
that point everything runs off a local dev server. Repo creation happens
through the GitHub website when you're ready.

**1.2 Content inventory**
Crawl the live Startseite and legal pages; record headlines, body copy,
image slots, and link targets into `docs/content-inventory.md`. This is the
checklist Stage 2 is verified against, so nothing silently drops.

Also confirms the real Impressum/Datenschutz URLs, since the ones in
`CLAUDE.md` proved unreliable.

**1.3 Design system extraction**
Pull the computed typography, color, spacing, and breakpoint values from the
live site's stylesheets and rebuild them as CSS custom properties. Reading
the actual stylesheet beats eyeballing screenshots, and it means Stage 3
restyling is a token change rather than a per-page edit.

**1.4 Asset placeholders**
Logos, team photos, and client logos come from you later. Until then,
correctly-dimensioned placeholders so the drop-in is a clean swap with no
reflow.

---

## Stage 2 — 1:1 rebuild

Faithful reproduction. Where the current site's copy is generic or stale, it
gets reproduced as-is — flagged in a list for Stage 3, not fixed here.

**2.1 Shared layout**
Header, nav, footer, design-system CSS from 1.3. Semantic HTML, mobile-first
responsive, meta/OG tags. Built once, consumed by every page.

**2.2 Startseite**
Sections in the live site's order:

hero → client logos → success stories → solutions grid → "Warum wir?" →
team (Willy Li, Ilya Volkov) → three-step process → footer

**2.3 Legal pages**
Impressum and Datenschutz, text ported verbatim. Structure and styling only
— no new legal copy.

**2.4 Custom 404**
Catches the deferred routes and anything else unmatched.

**2.5 QA**
- Responsive at mobile / tablet / desktop breakpoints
- Keyboard nav, contrast ratios, alt text, heading hierarchy
- Chrome, Firefox, Safari
- Playwright pass via the `webapp-testing` skill — click through every page,
  screenshot each breakpoint, assert no console errors
- Side-by-side diff against the live site using the 1.2 inventory
- Lighthouse against the current WordPress site for the before/after numbers

**2.6 Commit and stop**
Commit the completed replica. Report what's done, the QA results, and the
list of generic/stale copy spotted along the way.

> **Gate: I wait here for your go-ahead before touching Stage 3.**

---

## Stage 3 — Changes *(not started without approval)*

Held until Stage 2 is signed off. Listed for completeness only:

- Rewrites of sections flagged as generic during Stage 2
- Deep Reading Engine section — draft content in
  `docs/content-deep-reading-engine.md`
- Kontakt / "Kostenloses Erstgespräch" flow, once the backend is decided
- E-Rechnung and Ergebnisse, once Willy confirms URLs and content
- Content corrections and any new sections

Two known content gaps for Willy, relevant only when we reach this stage:
which of the three DRE draft framings to use, and the third use case, where
draft 3 cuts off mid-sentence after "Angebot". No claims or numbers get
invented to fill those — the auditability pitch is the product's whole
selling point.

---

## What I need from you

| # | What | Needed by |
|---|---|---|
| 1 | GitHub repo URL | Whenever ready — local until then |
| 2 | Logos, team photos, client logos | Whenever ready — placeholders until then |
| 3 | Sign-off on the Stage 2 replica | Gate before Stage 3 |
| 4 | Willy: DRE framing + the truncated third use case | Stage 3 |
| 5 | Willy: real URLs and content status for E-Rechnung / Ergebnisse / Kontakt | Stage 3 |

Nothing blocks starting Stage 1.

Per project rules, I won't run `git push` or open a PR without asking first,
every time.

---

## First session

Stage 1 end to end, then straight into 2.1 — layout scaffold running on a
local dev server you can open in a browser.
