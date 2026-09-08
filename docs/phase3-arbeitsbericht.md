# Phase 3 — Arbeitsbericht

Dokumentation des Arbeitsablaufs beim Neubau der KIBH-Website mit Claude Code.
Zeitraum **23. August bis 8. September 2026**, 12 Arbeitssitzungen an 15
Kalendertagen, 82 Commits.

Dieser Bericht beschreibt ausschließlich, was tatsächlich geschehen ist. Er ist
aus drei Quellen rekonstruiert: den vollständigen Sitzungstranskripten (275
Einträge), der Git-Historie und dem laufenden Protokoll in `PROGRESS.md`.
Zahlen ohne Quellenangabe sind gemessen, nicht geschätzt.

---

## 1. Ausgangssetup

### Werkzeuge

| | |
|---|---|
| Betriebssystem | Windows 11 Pro |
| Werkzeug | Claude Code im Terminal (Modelle Sonnet 5, ab 28.08. Opus 5) |
| Laufzeit | Node.js — ausschließlich für das Build-Skript |
| Sprachen | HTML, CSS, JavaScript. Kein Framework, kein Bundler |
| Abhängigkeiten | **null** — `package.json` hat keinen `dependencies`-Block |
| Python | nur für die Hilfswerkzeuge (Playwright, Bildkodierung) |
| Versionierung | Git, Remote auf GitHub |
| Hosting | Vercel, automatischer Deploy bei jedem Push auf `main` |

### Was zu Projektbeginn im Verzeichnis lag

Nur zwei Dinge: `CLAUDE.md` mit der Aufgabenstellung und ein `docs/`-Ordner mit
Willys Entwurfstexten. Kein Git-Repository, kein Code, keine Konfiguration.
Alles Weitere ist im Projekt entstanden.

### Der entscheidende Vorbereitungsschritt

Vor der ersten Codezeile wurde der Skill **`webapp-testing`** installiert — ein
Playwright-Werkzeug, mit dem Claude einen echten Browser steuert, Seiten
aufruft, scrollt, misst und Screenshots aufnimmt.

Das war rückblickend die folgenreichste Entscheidung des gesamten Projekts.
Ohne ihn hätte Claude die Originalseite nur als Quelltext lesen können. Mit ihm
konnte sie **angesehen** werden — und genau daran hängt der wichtigste Lernschritt
des Projekts (Schritt 8).

### Was im Projekt entstanden ist

71 versionierte Dateien: ein 141-zeiliges Build-Skript, das aus `src/` das
Verzeichnis `dist/` erzeugt; 12 Quellseiten; 4 033 Zeilen CSS; 601 Zeilen
JavaScript; zwei Playwright-Testskripte (`tests/qa.py`, `tests/compare.py`);
zwei Bildwerkzeuge (`tools/encode-webp.py`, `tools/cutout.py`); sechs
Dokumentationsdateien und das Sitzungsprotokoll `PROGRESS.md`.

---

## 2. Die 13 Arbeitsschritte

### Schritt 1 — Werkzeuge und Setup
**23.08., ca. 1 h**

Skills installiert, Verzeichnis gesichtet, Aufgabenstellung gelesen. Noch kein
Code, noch kein Repository.

### Schritt 2 — Planung
**23.08., ca. 1,5 h**

Auftrag: *„Can you make a plan for how we'll rebuild this website, step by
step?"*

Claude legte einen Stufenplan vor. Hari korrigierte ihn sofort in eine Richtung,
die für das ganze Projekt bestimmend blieb:

> „The plan is almost perfect. Omit the parts where you say I do not have web
> developing exp and where you explain some technical words. We do not need that
> in the plan. You can also use technical vocabulary. I can catch up."

Damit war der Ton gesetzt: technische Sprache, keine Erklärstücke, keine
Rücksicht auf fehlende Vorerfahrung. Der Stack wurde in derselben Nachricht
entschieden (Node.js). Ergebnis: `websiteSkeletonPlan.md`.

**Anmerkung:** Der Plan sah nach Stufe 2 einen Freigabe-Stopp vor. Diese
Stufenlogik wurde später aufgeweicht — siehe Schritt 11.

### Schritt 3 — Bestandsaufnahme des Originals
**23.08., ca. 1 h — Commits `4f251fd`, `c8f75eb`**

Die Originalseite wurde nicht abgeschrieben, sondern **vermessen**. Claude fuhr
sie mit Playwright ab und legte drei Dokumente an:

- `docs/design-system.md` — Farben, Schriftgrößen, Abstände, jeweils mit der
  Stelle, an der der Wert gemessen wurde
- `docs/url-map.md` — jede alte URL und ihre neue Entsprechung
- `docs/content-inventory.md` — die Checkliste, gegen die der Nachbau später
  geprüft wurde

Hier fiel schon der erste Befund über den Zustand des Originals auf: eine Liste
sichtbarer Defekte der Live-Seite.

### Schritt 4 — 1:1-Nachbau aller Seiten
**23.08., ca. 20 min — Commits `4dda33b`, `e3b02ff`**

Alle 10 Seiten in **einem** Durchgang. Das ist der Schritt, bei dem Claude Code
gegenüber Handarbeit am deutlichsten gewinnt: Struktur, Texte, Farben, Layout
und Navigation für zehn Seiten in gut zwanzig Minuten.

Direkt danach eine erste Performance-Messung gegen die Live-Seite. Die damals
notierte Zahl („24× leichter") war allerdings **falsch** — sie wurde auf einem
Stand gemessen, auf dem noch alle Bilder Platzhalter waren. Korrigiert erst am
03.09., siehe Schritt 11.

### Schritt 5 — Deployment
**23.08., ca. 40 min**

Hari gab das GitHub-Repository frei und erteilte die Push-Erlaubnis. Der erste
Vercel-Build **schlug fehl**: die Konfiguration zeigte auf ein
Ausgabeverzeichnis, das Vercel nicht erwartete. Nach der Korrektur lief der
Deploy und lief ab da bei jedem Push automatisch durch.

Ab hier gab es zwei Prüfumgebungen: `localhost:4173` und die öffentliche
Vercel-URL.

### Schritt 6 — Neuer Inhalt: Deep Reading Engine
**24.08., 27.08., 28.08. — Commits `196fe93`, `a4309b4`, `9a97e34`, `6b208ed`**

Die einzige wirklich **neue** Sektion des Projekts, alles andere war Nachbau.

Zwei Durchgänge, und der Unterschied zwischen ihnen ist aufschlussreich:

- **24.08.** — auf Basis der Entwurfstexte in `docs/`. Claude durfte aus drei
  überlappenden Entwürfen eine Fassung bauen.
- **27.08.** — Willy lieferte den finalen Text. Anweisung: *„Replace the DRE
  section content with the exact text below, word for word — do not rewrite,
  paraphrase, summarize, restructure, or 'fix' any of it."* Ausdrücklich
  einschließlich dem, was wie ein Tippfehler aussieht.

Danach eine kurze Korrekturrunde (vier Punkte), unter anderem die Entscheidung,
die Seite mit der Frageform statt mit dem CTA-Band zu schließen.

### Schritt 7 — Regelklärung und Prozess-Infrastruktur
**24.–25.08. — Commits `e572b86`, `869b284`, `e7d01bb`**

Zwei Weichenstellungen, die keine sichtbare Änderung an der Website waren, aber
die Zusammenarbeit prägten.

**a) Die Erlaubnis, Defekte überall zu beheben.** Hari:

> „If you see some errors on other sections, you are afraid to correct them. I
> mean by errors, like coding errors. Like if a text is overflowing its box …"

Claude hatte Layoutfehler in Sektionen gefunden, an denen es nicht arbeiten
sollte, und sie unangetastet gelassen — weil „nichts anderes anfassen" zu breit
ausgelegt worden war. Ab hier galt: **Darstellungsfehler werden ohne Rückfrage
korrigiert, inhaltliche Logik und Formulierungen nicht.** Diese Trennung hat bis
zum Projektende gehalten.

**b) `PROGRESS.md`.** Jede Sitzung endete damit, dass der Gesprächskontext
volllief. Die nächste Sitzung begann bei null. Hari ließ deshalb ein
Sitzungsprotokoll anlegen — ausdrücklich nicht für sich, sondern für Claude:

> „Not for me, but for Claude to keep track of what we've done so far."

Die erste Fassung wiederholte Projektziel und Regeln aus `CLAUDE.md` und wurde
zurückgewiesen: *„We already need to keep track of the progress."* Ergebnis ist
ein reines, datiertes Was-wurde-getan-Protokoll — am Projektende 819 Zeilen.

### Schritt 8 — Der 1:1-Wendepunkt
**25.–26.08., ca. 2 h — Commits `1e606fe`, `ddc4bbf`, `5c2d617`, `8ecbc81`**

**Der wichtigste Lernschritt des Projekts.**

Die E-Rechnung-Seite war nach Vorlage nachgebaut worden: Struktur, Texte, Farben
stimmten. Hari sah sie im Browser an und schrieb:

> „I notice that you just copied the texts and didn't do the animations and made
> the section like a raw html file."

Und in der Folgenachricht die Regel, die das Projekt neu ausrichtete:

> „Add all the animations. **I want the section 1:1 with what the user sees, not
> the code.** If you need screenshots, tell me. But better, run webapp-testing on
> the original website and see by yourself."

Der Fehler war methodisch. Claude hatte die Seite aus DOM-Struktur und
berechneten Stilwerten rekonstruiert. Was dabei systematisch verlorengeht:

1. **Bewegung.** Das Original blendet fast jedes Element beim Scrollen ein
   (Elementor `fadeInUp`, `fadeInLeft`). Im Quelltext steht davon nichts
   Sichtbares — die Elemente parken auf Deckkraft 0. Ohne die Animationen wirkte
   der Nachbau wie ein statisches Dokument neben dem Original.
2. **Hintergründe und Atmosphäre.** Drei Bänder des Originals stehen auf
   schwarzem Grund mit einem türkis-blauen Leuchten. Aus den berechneten Stilen
   ließ sich nur „schwarz plus Hintergrundbild" ablesen; die Annäherung mit
   einem gedämpften Verlauf traf die Wirkung nicht. Hari musste auch das noch
   einmal einzeln monieren.

Die Methode ab hier: **die Originalseite mit Playwright fahren, so scrollen wie
ein Besucher, an mehreren Bildschirmbreiten Screenshots machen und Band für Band
vergleichen.** Nicht mehr aus DOM und `getComputedStyle` schließen.

### Schritt 9 — Seite-für-Seite-Abgleich gegen das Original
**28.–30.08., ca. 10 h — 28 Commits von `b1b1c11` bis `71585c3`,
davon 8 reine Protokolleinträge**

Die längste Phase. Mit der neuen Methode wurde jede Seite noch einmal gegen ihr
Original geprüft.

| Vorgang | Datum | Commits |
|---|---|---|
| Vier Kundenstimmen auf `/ergebnisse/` ergänzt | 28.08. | `a9fd894`, `d0d5cc8`, `cb92ddb` |
| Schriften: Verdana für Fließtext, Mulish für Überschriften | 28.08. | `b1b1c11` |
| Startseite komplett gegen das Original neu aufgebaut | 28.08. | `60fb6e2` |
| Ergebnisse-Seite, Karten, Hero, Footer-Quicklinks | 29.08. | `f8852a8` – `66e3cff` |
| Impressum und Vertraulichkeit wortgetreu übernommen | 29.08. | `6ebb486` |
| Kontakt-Seite gebaut | 29.08. | `f4b13f7`, `ddf82a2` |
| Vier Fallstudienseiten auf das U2care-Design vereinheitlicht | 30.08. | `5ca9b9c`, `d40edd7` |
| Echte Fotos und Logos eingesetzt, alle Platzhalter ersetzt | 30.08. | `b395903` – `875dc5e` |
| Favicon des Originals übernommen | 30.08. | `71585c3` |

Der Schriftenwechsel begann mit einer Rückfrage von Hari — *„you said the font
does not match 100 %? Why?"* —, also mit einer Nachfrage zu einer Nebenbemerkung,
nicht mit einem Auftrag. Aus der Antwort wurde eine eigene Aufgabe.

Bei den Assets zeigte sich das übliche Muster: erste Lieferung, dann drei
Nachträge (fehlende Logos, Kreisform statt Kachel, vergessenes Footer-Logo).

### Schritt 10 — Verworfener Design-Versuch und Rollback
**30.08., ca. 1,5 h — vollständig verworfen, kein Commit erhalten**

Hari ließ die Seite gegen acht Prinzipien hochwertigen Webdesigns prüfen und
einen Plan schreiben, ausdrücklich ohne Umsetzung. Danach:

> „Execute all the stages in a batch and give me the link to the local host when
> you are done, so that I can see the difference. If I don't like it, we can just
> delete that commit and try again."

Das Ergebnis wurde nach Sichtprüfung komplett verworfen:

> „No, don't push, I don't like it. It looks worse. Delete that commit and the
> plan in the polish md file."

**Das ist der einzige vollständig verlorene Arbeitsblock des Projekts** — rund
anderthalb Stunden. Bemerkenswert ist, wie billig der Rückbau war: ein Commit
gelöscht, der Stand war wieder sauber. Die Möglichkeit, einen Versuch
folgenlos wegzuwerfen, war vorher ausdrücklich eingeplant worden.

### Schritt 11 — Qualitätspässe
**02.–04.09., ca. 6 h — Commits `ae99db8` bis `0285257`**

Vier voneinander unabhängige Durchgänge über die ganze Seite:

**Mikrointeraktionen (02.09.)** — sechs dezente Bewegungseffekte, ausdrücklich
zurückhaltend. Nachbesserung nötig: *„I can't see the cursor glow"* — der Effekt
war zu schwach eingestellt und wurde nur auf einer Seite ausgespielt.

**Responsive-Audit (03.09.)** — systematische Prüfung an mehreren echten
Bildschirmbreiten, nicht an einer generischen „Mobilansicht". Direkt danach ein
echter Funktionsfehler, den nur Hari finden konnte, weil er ein Telefon in der
Hand hatte:

> „With a phone, when I click on 'Vertraulichkeit', I land on the false page,
> sometimes the right page."

Ursache: das geschlossene Navigationsmenü blieb unsichtbar über der Seite liegen
und fing Berührungen ab. Am Schreibtisch nicht reproduzierbar.

**Die Qualitätsfrage (03.09.)** — Hari fragte offen: *„What is in your opinion
missing on our website so that it looks like a 10 000 Euro website?"* Claude
schlug drei Stufen vor. Antwort:

> „Stage 1 and 2 are bad. Only commit stage 3."

Das ist das Muster des ganzen Projekts im Kleinen: Vorschläge werden einzeln
angenommen oder abgelehnt, nicht als Paket.

**Bilder und Schriften (03.–04.09.)** — alle 25 Bilder auf WebP umkodiert,
`assets/img` von **6,6 MB auf 789 KB**. Dabei wurde die falsche Zahl aus Schritt
4 korrigiert: statt „24× leichter" gilt gemessen **6,8× leichter beim Laden**
und **4,4× vollständig gelesen**. Nachgewiesen, dass sich dabei kein Pixel
verschob: Screenshots aller 12 Seiten vorher/nachher, identisch bis auf einen
Pixel, der eine falsche Bildabmessung korrigierte.

### Schritt 12 — Willys Review
**05.09., ca. 2,5 h — Commits `30a70d2`, `11dc074`, `e929dd4`**

Der erste externe Blick. Willy schickte zehn konkrete Punkte: Kopfleiste zu
niedrig, Überschriftsfarbe uneinheitlich, fehlendes türkises Panel hinter dem
Roboter, Kundenlogos ohne Kachel, zu große Abstände nach den CTA-Bändern, eine
Karte austauschen, Teamfotos zu groß, DRE-Hero aufteilen, E-Rechnung strikt 1:1,
Label entfernen.

Punkt 9 ist der interessanteste: er **kehrte drei frühere Entscheidungen von
Hari um**. E-Rechnung sollte ohne jede Abweichung dem Original entsprechen. Vor
der Korrektur wichen 56 Textblöcke in der Schriftfamilie ab, 17 in der Größe, 30
in der Zeilenhöhe; danach null in Größe, Gewicht und Farbe.

Dabei kam die Frage auf, wie weit „1:1" reicht, wenn das Original selbst kaputt
ist: auf der Live-Seite hat ein Band seinen Hintergrund verloren, die weiße
Überschrift steht auf Weiß und ist unsichtbar. Haris Entscheidung: **das ist ein
Fehler, kein Design — unsere funktionierende Fassung bleibt.** Bewusste
Inkonsistenzen des Originals wurden dagegen mitkopiert.

Anschließend fünf eigene Nachträge von Hari zum Reviewstand.

### Schritt 13 — Letzte Assets, Produktisierung, Abschluss
**05.–08.09., ca. 2,5 h — Commits `7ea3dbd` bis `ede6c0c`**

Willys Roboterbild wurde geliefert und musste freigestellt werden — Hintergrund
entfernen, Kanten weich auslaufen lassen. Dafür entstand `tools/cutout.py`.
Danach die Kopfleiste auf 92 px feinjustiert („bigger than the one before,
smaller than the one now").

Am 05./06.09. entstanden zwei Dateien, die nicht zur Website gehören, sondern zum
Geschäft: eine wiederverwendbare Auftragsvorlage und eine Projektvorlage für
künftige Kunden. Beide wurden am 08.09. wieder aus dem Repository entfernt,
nachdem auffiel, dass es öffentlich ist.

Letzte Korrektur am 08.09.: Der Button „Kostenloses Erstgespräch" hatte in der
Kopfleiste auf der Startseite eine andere Form als auf allen anderen Seiten.
Ursache war eine seitenspezifische Regel, die auf ein gemeinsames Element
durchschlug. Einheitlich gelöst (`ede6c0c`).

---

## 3. Der wiederkehrende Arbeitszyklus

Die Kategorisierung oben liest sich linear. **Das war die Arbeit nicht.** Sie
lief rund vierzigmal durch dieselbe Schleife:

> **Auftrag → Ausführung → Sichtprüfung im Browser → Korrektur → `push it`**

Die Zahlen aus den Transkripten belegen das:

| Art der Nachricht | Anzahl |
|---|---|
| Lange Auftragsprompts (mehrteilige Aufgaben) | 26 |
| Kurze Anweisungen (überwiegend Korrekturen) | 81 |
| Screenshots von Hari | 33 |
| Operative Befehle (`push it`, `local host`) | 27 |
| Kontext-Kompaktierungen (je Befehl + Zusammenfassung) | 11 × 2 |
| **Summe der Transkripteinträge** | **275** |

**Auf jeden großen Auftrag kamen etwa drei kurze Korrekturanweisungen.** Kein
einziger großer Auftrag lief ohne Nachbesserung durch.

### Wie geprüft wurde

Hari hat in 15 Kalendertagen **kein einziges Mal Code gelesen**. Geprüft wurde
ausschließlich das gerenderte Ergebnis, auf zwei Wegen:

- *„local host"* — 27-mal angefordert, um selbst im Browser nachzusehen
- 33 Screenshots, die er zurückschickte, mit dem Problem darauf

Die Korrekturen waren entsprechend formuliert: nicht „ändere die CSS-Regel X",
sondern *„the box is a little bit chaotic and too narrow"*, *„make Martin
horizontal again"*, *„the yellow line under KI-Lösungen should be one, not two"*.

Genau daraus folgt der Wendepunkt aus Schritt 8: Wenn ausschließlich das
gerenderte Bild bewertet wird, muss auch ausschließlich gegen das gerenderte
Bild gearbeitet werden.

### Wer was entschieden hat

- **Hari** — Aufträge, Prioritäten, Annahme oder Ablehnung jedes Vorschlags,
  jede Push-Freigabe. Alles, was das Aussehen der Seite änderte.
- **Claude** — technische Umsetzung, Messung, Tests, das Aufdecken und Beheben
  von Darstellungsfehlern.
- **Willy** — Inhalte, das Review, die Entscheidung über strittige Punkte.

Vorschläge, die das Aussehen betrafen, wurden nie eigenmächtig umgesetzt.
Mehrfach lehnte Hari messbar begründete Änderungen ab (Kontrastwerte,
Zeilenlängen) — die Messung allein war nie Rechtfertigung genug.

---

## 4. Stolpersteine

Ehrlich aufgeführt, mit Kosten. Das ist der Teil, der die Fallstudie belastbar
macht.

### Methodisch

**1. Der 1:1-Irrtum (Schritt 8) — der teuerste.** Aus DOM und berechneten Stilen
rekonstruiert statt aus dem gerenderten Bild. Kostete den kompletten Neubau der
E-Rechnung-Seite und schlug später noch einmal durch, als das gleiche Muster bei
Startseite und Ergebnisse auffiel.

**2. Der verworfene Design-Versuch (Schritt 10).** Rund 1,5 h vollständig
weggeworfen. Die Ursache war kein Fehler, sondern eine Geschmacksfrage, die sich
erst am Ergebnis entscheiden ließ.

### Werkzeugbedingt

**3. Kontextverlust — elf Kompaktierungen.** Jede längere Sitzung lief voll und
musste zusammengefasst werden; nach jedem Neustart fehlte Claude der
Projektstand. `PROGRESS.md` existiert genau deswegen. Das ist kein Randproblem,
sondern der Grund für eine eigene Datei und für Zeit, die in jeder Sitzung ins
Wiedereinlesen ging.

**4. Nutzungslimits.** Die Arbeit wurde dreimal mitten in einer laufenden
Aufgabe unterbrochen (*„can you resume where you were interrupted? The limit
barrier should be gone now"*). Planbar ist das nicht.

**5. Nicht reproduzierbare Testergebnisse.** Ein Prüfskript meldete bei
identischem Code in aufeinanderfolgenden Läufen unterschiedliche Ergebnisse —
eine Zeitabhängigkeit beim Laden von Bildern. Konsequenz: bei einem
überraschenden Sprung erst wiederholen, dann glauben.

**6. Windows-Eigenheiten.** Zeilenenden und Zeichenkodierung haben mehrfach
Dateien beschädigt; Python ist nicht im Standardpfad. Beides ist im Projekt
dokumentiert, damit es nicht erneut Zeit kostet.

### Technisch

**7. Falsche Zielseite beim Antippen.** Nur auf einem echten Telefon
reproduzierbar (Schritt 11). Ein unsichtbares Element fing Berührungen ab.

**8. Einzelfallen mit realem Zeitverlust** — die CSS-Einheit `ch`, die deutlich
weniger Zeichen fasst als vermutet; `darken` statt `multiply` beim Einbetten
undurchsichtiger Logos; ein Favicon, das im Browser ohne Fenster nie angefragt
wird und deshalb fälschlich als fehlend gemeldet wurde. Jede kostete einmal
Zeit und ist danach dokumentiert.

**9. Die Bildlast.** Nachdem die echten Bilder eingesetzt waren, war die Seite
zeitweise rund **zwanzigmal schwerer**, als die eigene Performance-Messung
behauptete — weil diese Messung noch aus der Platzhalter-Phase stammte. Erst am
03.09. korrigiert. **Lehre: eine Kennzahl verfällt, wenn sich die Grundlage
ändert.**

### Beim Original

**10. Die Vorlage ist selbst defekt.** Alle Unterseiten-Permalinks liefern 404
und antworten nur unter einem Umweg-Pfad; das Kundenlogo-Karussell liefert
kaputte Bilder; ein Band hat seinen Hintergrund verloren, wodurch weißer Text
auf weißem Grund steht. Das erzwang eine eigene Regelentscheidung (Schritt 12) —
und ist zugleich ein starkes Verkaufsargument für die Migration.

---

## 5. Zeitaufwand

### Messmethode

Aus den Zeitstempeln der Sitzungstranskripte. Als Arbeitszeit gilt der Abstand
zwischen zwei aufeinanderfolgenden Nachrichten, **sofern er 20 Minuten nicht
überschreitet** — längere Lücken sind Pausen. Zusätzlich ist die Variante mit
45-Minuten-Grenze als obere Schranke angegeben. Alle Zeiten in Lokalzeit
(MESZ), passend zu den Commit-Zeitstempeln.

Gemessen wird die **Zeit am Rechner**, nicht die reine Rechenzeit von Claude.
Wartezeiten, Sichtprüfungen im Browser und das Formulieren der Prompts sind
enthalten — das ist die Zahl, die für eine Kalkulation zählt.

### Pro Tag

| Datum | Schritte | Aktiv (20 min) | Obergrenze (45 min) |
|---|---|---:|---:|
| 23.08. | 1–5 | 2 h 05 | 4 h 28 |
| 24.08. | 6, 7 | 1 h 18 | 1 h 18 |
| 25.08. | 7, 8 | 1 h 12 | 1 h 12 |
| 26.08. | 8 | 1 h 01 | 1 h 01 |
| 27.08. | 6 | 0 h 40 | 1 h 04 |
| 28.08. | 6, 9 | 3 h 00 | 3 h 00 |
| 29.08. | 9 | 2 h 24 | 3 h 30 |
| 30.08. | 9, 10 | 4 h 59 | 5 h 20 |
| 31.08. | 10 (Abschluss) | 0 h 01 | 0 h 01 |
| 02.09. | 11 | 1 h 10 | 1 h 44 |
| 03.09. | 11 | 3 h 39 | 3 h 59 |
| 04.09. | 11 | 1 h 13 | 1 h 13 |
| 05.09. | 12, 13 | 2 h 24 | 2 h 47 |
| 06.09. | 13 | 1 h 44 | 2 h 12 |
| 08.09. | 13 | 0 h 27 | 0 h 27 |
| **Summe** | | **27 h 24** | **33 h 24** |

Die Tageswerte sind auf volle Minuten abgerundet; die Spalte addiert sich
deshalb auf 27 h 17 bzw. 33 h 16. Die Summenzeile nennt den ungerundeten Wert.

### Pro Arbeitsschritt

| Schritt | Aufwand |
|---|---:|
| 1 — Werkzeuge und Setup | ~1 h |
| 2 — Planung | ~1,5 h |
| 3 — Bestandsaufnahme des Originals | ~1 h |
| 4 — **1:1-Nachbau aller 10 Seiten** | **~20 min** |
| 5 — Deployment | ~40 min |
| 6 — Deep Reading Engine (zwei Durchgänge) | ~2 h |
| 7 — Regelklärung, `PROGRESS.md` | ~1 h |
| 8 — Der 1:1-Wendepunkt | ~2 h |
| 9 — Seite-für-Seite-Abgleich | ~10 h |
| 10 — Verworfener Versuch (Totalverlust) | ~1,5 h |
| 11 — Qualitätspässe | ~6 h |
| 12 — Willys Review | ~2,5 h |
| 13 — Letzte Assets und Abschluss | ~2,5 h |

### Was daran auffällt

**Der eigentliche Bau war der kürzeste Schritt.** Zehn Seiten in gut zwanzig
Minuten. Alles davor (Planung, Vermessung) und alles danach (Abgleich, Korrektur,
Review) kostete das Fünfzigfache.

Die Zeit ging in **Genauigkeit**, nicht in Erzeugung: Schritt 9 allein — der
Abgleich Seite für Seite gegen das Original — ist mehr als ein Drittel des
gesamten Aufwands.

Nicht in diesen Zahlen enthalten: das Erstellen dieses Berichts.

---

## 6. Bewertung: Claude Code gegenüber WordPress

Nüchtern, als Zulieferung für die Fallstudie. Nur Aussagen, die in diesem
Projekt gemessen oder erlebt wurden.

### Was klar dafür spricht

**Geschwindigkeit beim Erzeugen.** Zehn Seiten in gut zwanzig Minuten. Für die
gesamte Website inklusive Recherche, Deployment, Kundenreview und Dokumentation:
**27 bis 33 Stunden.**

**Das Ergebnis ist messbar leichter.** Beim Laden 6,8×, vollständig gelesen
4,4×. Das größte Einzelstück ist das Stylesheet: WordPress liefert 1 363 KB
zusammengefasstes CSS aus, davon nutzt die Seite einen Bruchteil — hier sind es
126 KB.

**Keine Abhängigkeiten, keine Plugins, keine Updates.** `package.json` hat keinen
`dependencies`-Block. Es gibt nichts, was veralten, brechen oder eine
Sicherheitslücke aufreißen kann.

**Änderungen sind billig und umkehrbar.** Die letzte Korrektur des Projekts —
eine uneinheitliche Button-Form auf allen 12 Seiten — dauerte wenige Minuten,
inklusive automatisierter Prüfung. Ein verworfener Versuch kostete einen
gelöschten Commit.

**Prüfbarkeit.** Ein Testskript prüft 11 Seiten an 5 Bildschirmbreiten auf
Überläufe, abgeschnittene Texte, tote Links und Konsolenfehler. Dieselbe
Zusicherung gibt es bei WordPress nicht.

### Was Aufwand kostet

**Der Abgleich, nicht der Bau.** Zwei Drittel der Zeit gingen dafür drauf, das
Ergebnis dem Original anzugleichen. Wer eine visuell exakte Migration verkauft,
verkauft diese Arbeit — nicht die zwanzig Minuten Erzeugung.

**Es braucht einen Menschen, der hinsieht.** Alle 33 Screenshots und praktisch
jede Korrektur kamen daher, dass Hari die Seite im Browser beurteilte. Zwei
Fehler waren nur so auffindbar: die falsche Zielseite beim Antippen auf einem
echten Telefon und die fehlenden Animationen. **Ohne diese Prüfschleife wäre die
Seite fertig und falsch gewesen.**

**Prompt-Qualität ist Projektqualität.** Die großen, präzise formulierten
Aufträge lieferten brauchbare Ergebnisse; die vagen erzeugten Nacharbeit. Das
ist eine Fähigkeit, die eingekauft oder erlernt werden muss.

**Werkzeugbedingte Reibung.** Kontextverluste, Nutzungslimits und
plattformbedingte Eigenheiten haben real Zeit gekostet (Abschnitt 4).

### Fazit

Für eine Website dieses Zuschnitts — überschaubare Seitenzahl, überwiegend
Inhalt, wenig Serverlogik — ist der Ansatz **wirtschaftlich klar überlegen**,
solange jemand mit Urteilsvermögen die Prüfschleife übernimmt. Der Wert liegt
nicht darin, dass Claude Code schnell Seiten erzeugt, sondern darin, dass
**Korrekturen fast nichts kosten**: Das erlaubt die vielen kleinen Durchgänge,
aus denen am Ende die Genauigkeit entsteht.

Was hier **nicht** belegt ist: das Verhalten bei umfangreicher Serverlogik, bei
mehreren hundert Seiten oder bei Redakteuren, die Inhalte selbst pflegen wollen.
Der Punkt „Redaktion durch den Kunden" ist der offene Punkt gegenüber WordPress
und sollte in der Fallstudie ehrlich benannt werden.

---

## Quellen

| Nachweis | Datei |
|---|---|
| Sitzungsprotokoll, alle Termine | `PROGRESS.md` |
| Ursprünglicher Plan (Schritt 2) | `websiteSkeletonPlan.md` |
| Aufgabenstellung und Projektregeln | `CLAUDE.md` |
| Messwerte alt/neu, Methodik, Vorbehalte | `docs/performance-baseline.md` |
| Design-Werte mit Fundstelle | `docs/design-system.md` |
| URL-Zuordnung alt → neu | `docs/url-map.md` |
| Inhaltsprüfliste | `docs/content-inventory.md` |
| Commit-Historie | `git log` — 82 Commits, 23.08.–08.09. |
