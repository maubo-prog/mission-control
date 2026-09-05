# Mission Control Autopilot

Serverloses, kostenloses Kennzahlen-Dashboard fuer den Creator-Account @spacefactswow
(TikTok, YouTube Shorts, Instagram Reels). Betreiber ist ein Solo-Creator, kein Entwickler.
Mission: 10.000 TikTok-Follower und 100k TikTok-Views in 30 Tagen.
Marke wie in der Videoproduktion: Gelb #FFEC00 auf Tiefblau, Montserrat.
Videoarbeit selbst laeuft nicht hier, sondern ueber die Konto-Skills (spacefacts-*) und einen eigenen Auftrag.

## Sprache

Antworten, Commit-Messages, Kommentare, Doku und UI-Texte auf Deutsch, du-Form.
Code-Bezeichner (Variablen, Funktionen, JSON-Schluessel) bleiben Englisch.
Keine Gedankenstriche, keine Emojis in Texten, die du erzeugst.

## Dateien

- `update.py`: taeglicher Abruf der oeffentlichen Profilzahlen, nur Standardbibliothek, schreibt `docs/data.json`. `main()` haengt hinter `if __name__`, Import im Test ist gefahrlos.
- `.github/workflows/update.yml`: startet den Abruf per Cron und committet `docs/data.json` direkt auf main. Der Bot ist der einzige legitime Schreiber dieser Datei.
- `docs/index.html`: Ein-Datei-Dashboard, Vanilla JS, kein Build. Wird ueber GitHub Pages aus `/docs` oeffentlich ausgeliefert.
- `docs/data.json`: Zeitreihe aller Messwerte. Oeffentlich lesbar, waechst taeglich um einen Eintrag.
- `README.md`: Schritt-fuer-Schritt-Anleitung fuer Nicht-Entwickler. Nicht mit Entwicklerdetails zumuellen.

Alles unter `docs/` ist oeffentlich im Netz. Dort niemals private Daten ablegen.

## Befehle

```
python3 -m py_compile update.py                 # Syntax
python3 -m json.tool docs/data.json > /dev/null  # JSON gueltig
python3 -m unittest discover -s tests -v         # Tests
python3 tools/check_data.py                      # Schema von data.json
python3 tools/check_html.py                      # Dashboard-Struktur und IDs
python3 tools/stats.py --days 30                 # Zahlen fuer Berichte
cd docs && python3 -m http.server 8000           # Dashboard lokal ansehen
```

Achtung bei `python3 update.py`: das macht echte Netzabrufe und ueberschreibt den heutigen
Eintrag in `docs/data.json`. Nur nach Rueckfrage, danach immer `git checkout docs/data.json`.

## Datenschema docs/data.json

`{updated, handles, entries: [{date, tiktok:{f,l}, youtube:{f,v}, instagram:{f}}]}`

- `f` Follower, `l` Likes, `v` Views. Jeder Wert ist int oder null, nie String, nie 0 als Ersatz fuer null.
- `date` im Format YYYY-MM-DD, eindeutig pro Tag, aufsteigend sortiert, maximal 400 Eintraege.
- `docs/index.html` haengt an genau diesen Schluesseln. Umbenennen bricht das Dashboard.
- `tiktok.v` ist als optionaler Schluessel vorgesehen, wird vom Dashboard aber noch nicht gelesen:
  `series()` setzt `tiktok.v` fest auf null und nimmt den Wert nur aus dem localStorage.

## Invarianten

- `merge()`: neue Werte gewinnen, aber null ueberschreibt nie einen guten alten Wert.
- Nur Standardbibliothek (`urllib`, `re`, `json`, `datetime`, `pathlib`). Keine neuen Abhaengigkeiten, kein Build-Step, kein Framework.
- Der Abruf-Workflow braucht nur `contents: write`. Neue Workflows bekommen die kleinstmoeglichen Rechte.
- Ein fehlgeschlagener Abruf schreibt null, er darf nie den Prozess abbrechen oder alte Werte loeschen.

## Nicht anfassen ohne Rueckfrage

- `docs/data.json` von Hand oder direkt auf main aendern (der Bot schreibt dort, das gibt Konflikte).
- `HANDLES` in `update.py`, die Cron-Zeit in `update.yml`, die Datei `update.yml` insgesamt.
- `docs/` als Pages-Wurzel, den Dateinamen `docs/index.html`.

## Bekannte Schwaechen (Stand 2026-09-04)

- YouTube-Views sind falsch: die Regex greift die Aufrufe eines einzelnen Videos, nicht die Kanalsumme.
- Instagram-Follower sind durchgaengig null, der JSON-Endpunkt und die Profilseite liefern nichts mehr.
- TikTok-Likes werden seit 12.08. auf volle 100 gerundet geliefert.
- TikTok-Ausfaelle am 23.08. und 28.08., ohne Alarm bemerkt niemand so etwas.
- TikTok-Views und Instagram-Nachtraege liegen nur im localStorage des Handys, nicht im Repo.

Diese Punkte sind dokumentiert, nicht offen zur spontanen Reparatur. Fixes laufen ueber `/scraper-fix` und einen eigenen PR.

## Arbeitsweise

- Nie auf main pushen, nie main direkt aendern. Immer Branch `claude/<thema>`, kleiner PR, Merge macht der Betreiber.
- Commit-Stil deutsch und knapp: `Fix: ...`, `Setup: ...`, `Doku: ...`.
- Vor jedem Commit die Checks aus dem Abschnitt Befehle laufen lassen, die zur Aenderung passen.
- Erkundung ueber mehrere Dateien an den eingebauten Explore-Subagenten geben.
- Lange Diffs und Workflow-Logs an den Agent `pruefer` geben, nicht selbst in den Hauptkontext holen.

## Kontext-Hygiene

- `docs/data.json` nie mit Read oeffnen, das ist in `.claude/settings.json` gesperrt. Zahlen kommen aus `python3 tools/stats.py`, Korrekturen aus `/data-repair`.
- Suche ueber mehrere Dateien an den Explore-Subagenten, lange Diffs und Logs an `pruefer`. Nur Ergebnisse zurueck in den Hauptkontext.
- Jede Datei einmal ganz lesen, danach nur noch gezielt mit Grep.
- Grosse Ausgaben kuerzen: `| tail -20`, `--stat`, `-q`.
- Bei mehr als zwei betroffenen Dateien oder Aenderungen am Schema zuerst Plan-Modus, dann umsetzen.
- Nach abgeschlossenen Aufgaben `/handoff` vorschlagen. Antworten kurz halten, keine ungefragten Code-Erklaerungen.

## Zeit

Cron `30 4 * * *` ist UTC, also 06:30 MESZ und 05:30 MEZ. GitHub startet Cron-Jobs oft
10 bis 40 Minuten spaeter. Das Datum im Eintrag ist das UTC-Datum des Runners, nicht die Ortszeit.

## Session-Uebergabe

@.claude/handoff.md
