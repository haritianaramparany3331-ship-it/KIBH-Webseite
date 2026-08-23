# KIBH — Content inventory (live site)

Extracted from the live pages. This is the checklist the Stage 2 replica is
verified against.

## Global

**Nav:** Startseite · E-Rechnung · Ergebnisse ▾ (Potenzial Analyse,
Kommunikation / Management, U2care, Automatische Rechnungsprüfung) ·
Warum wir? · **CTA:** Kostenloses Erstgespräch

**Footer:** KIBH / KI Beratung Hessen · "Ihr Weg zur KI-Exzellenz" ·
Quicklinks (nav mirror) · Rechtliche Hinweise (Vertraulichkeit, Impressum) ·
"Copyright © KI Beratung Hessen – Alle Rechte vorbehalten."

## Pages

| Page | Key content |
|---|---|
| **Startseite** | Hero (eyebrow "Transformieren Sie Ihr Unternehmen mit künstlicher Intelligenz", h1 "Ihr Partner für maßgeschneiderte KI-Lösungen", h2 "im Mittelstand") → client logos (7, `1.png`–`7.png`) → 3 success stories → 9 solution cards → Warum wir? (4 pillars) → team (Willy Li, Ilya Volkov) → 3-step process → CTA |
| **E-Rechnung** | Hero "E-Rechnung wird Pflicht! Sind Sie bereit?" → 4 risks → 4 questions → 5 advantages → 2 solution tiers (Große / Kleine Lösung) with 5-step + 4-step breakdowns |
| **Ergebnisse** | 7 case-study cards: Prozessautomatisierung (U2care), Potenzial Analyse, Fehlerquoten, Rechnungsprüfung, Kundenonboarding (JJ Real Estate), Rechnungsverarbeitung (Zrakic), + Newway testimonial |
| **Potenzial Analyse** | Testimonial (Hinnerbäcker) → 3 steps → "Das Ergebnis" (4 ✓ items) |
| **Kommunikation** | Case Study → testimonial → Ausgangssituation. **Sections "Erkenntniss", "Lösung", "Probleme" are empty headings on the live site** |
| **U2care** | Case study → Kundenzitat → Ausgangssituation → Lösung (3 Kernpunkte) → Ergebnisse |
| **Automatische Rechnungsprüfung** | Case Study → use case narrative → 3 ✓ deliverables → Ergebnis |
| **Kontakt** | Rotating headline "Wir freuen uns darauf, / deine Arbeit zu erleichtern. / dich kennen zu lernen. / zusammen zu arbeiten." + **Calendly embed** |
| **Impressum** | I Robot – You Profit GmbH, Fauerbacher Straße 41, 61169 Friedberg · VAT §27a: DE3572304466 · Willy Li · kontakt@kiberatunghessen.com |
| **Vertraulichkeit** | 9-section privacy policy |

## Booking

Live site embeds **Calendly**:
`https://calendly.com/ilya-den-volkov/kostenlose_strategieanalyse`

Per instruction, Stage 2 ships a styled **placeholder** in its place; all
"Termin buchen" / "Kostenloses Erstgespräch" buttons route to `/kontakt/`.
Wiring the real embed later is a one-block swap.

---

## Defects found on the live site

Fixing these in Stage 2 per your "fix design errors / nothing should lead
nowhere" instruction.

| # | Issue | Fix |
|---|---|---|
| 1 | **"Warum wir?" anchor mismatch** — nav links to `/#about`, on-page button links to `#warum`. One of them is broken. | Single consistent `#warum-wir` anchor |
| 2 | **Kontakt linked 3 ways** — `/index.php/Kontakt`, `/index.php/Kontakt/`, `/index.php/kontakt/`. Capitalised variants are separate URLs. | Normalise to `/kontakt/` |
| 3 | **Case-study cards drop trailing slash** — `/index.php/u2care`, `/index.php/kommunikation`, `/index.php/potenzial-analyse` | Consistent trailing slashes |
| 4 | **`/index.php/` prefix on every inner URL** — WordPress permalink misconfiguration | Clean URLs, 301s from old paths |
| 5 | **Zero-width space** (`U+200B`) inside "Potenzial Analyse​" in every nav | Strip |
| 6 | **`rechnungsprufung`** missing umlaut transliteration | `rechnungspruefung` |
| 7 | **`#76ABAE` vs `#77ABAE`** — near-duplicate accent, almost certainly a typo | Normalise to `#76ABAE` |
| 8 | **Typo "Erkenntniss"** → Erkenntnis | Fix |
| 9 | **Mixed quote marks** — `"..."` vs `„...“` vs `"...“` in testimonials | Normalise to German `„…“` |
| 10 | **Kommunikation page is unfinished** — 3 empty section headings | Omit the empty headings; flag for Willy |
| 11 | **Impressum is half-English** ("Information", "Contact", "Responsible Representative", "VAT according to") on a German site | Translate to German |

Items 10 and 11 touch content rather than markup — flagging them here; say
the word if you'd rather they stay verbatim.
