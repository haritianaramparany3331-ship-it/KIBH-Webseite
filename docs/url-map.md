# KIBH — Live site URL map

## The `/index.php/` finding

Every inner page on the live site is served under an **`/index.php/` path
prefix**:

```
https://kiberatunghessen.com/index.php/e-rechnung/     → 200
https://kiberatunghessen.com/e-rechnung/               → 404
```

This is a WordPress permalink misconfiguration — the rewrite rules that
normally strip `index.php` from URLs aren't active, so WordPress falls back
to including it literally. It's why my first checks reported these pages as
missing. **They all exist and all return 200.**

## Verified pages

| Live URL | Status | Page |
|---|---|---|
| `/` | 200 | Startseite |
| `/index.php/e-rechnung/` | 200 | E-Rechnung |
| `/index.php/ergebnisse/` | 200 | Ergebnisse |
| `/index.php/potenzial-analyse/` | 200 | Ergebnisse → Potenzial Analyse |
| `/index.php/kommunikation/` | 200 | Ergebnisse → Kommunikation/Management |
| `/index.php/u2care/` | 200 | Ergebnisse → U2care |
| `/index.php/automatische-rechnungsprufung/` | 200 | Ergebnisse → Automatische Rechnungsprüfung |
| `/index.php/kontakt/` | 200 | Kontakt |
| `/index.php/impressum/` | 200 | Impressum |
| `/index.php/elementor-page-689/` | 200 | Unidentified — likely Vertraulichkeit/Datenschutz |

Note `/index.php/Kontakt` also appears with a capital K, linked from the
page. Same page, inconsistent casing in the source.

## Implications for the rebuild

**We should not reproduce the `/index.php/` prefix.** It's a defect, it's
ugly, and it exists only because of a broken WordPress setting. Clean URLs
on the new site:

| New URL | Replaces |
|---|---|
| `/` | `/` |
| `/e-rechnung/` | `/index.php/e-rechnung/` |
| `/ergebnisse/` | `/index.php/ergebnisse/` |
| `/ergebnisse/potenzial-analyse/` | `/index.php/potenzial-analyse/` |
| `/ergebnisse/kommunikation/` | `/index.php/kommunikation/` |
| `/ergebnisse/u2care/` | `/index.php/u2care/` |
| `/ergebnisse/automatische-rechnungspruefung/` | `/index.php/automatische-rechnungsprufung/` |
| `/kontakt/` | `/index.php/kontakt/` |
| `/impressum/` | `/index.php/impressum/` |
| `/datenschutz/` | `/index.php/elementor-page-689/` |

Two notes on that table:

- `rechnungsprufung` in the original is missing its umlaut transliteration.
  Correct German would be `rechnungspruefung`. Worth fixing.
- Old URLs should get 301 redirects to the new ones so any existing search
  ranking and inbound links survive the move. Cheap to add on Vercel.

## Open question for Willy

`/index.php/elementor-page-689/` has an auto-generated Elementor slug,
meaning nobody ever gave it a proper title. It's linked from the footer
where `CLAUDE.md` says "Vertraulichkeit (Datenschutz)" should be — needs
confirmation that it is in fact the privacy policy.
