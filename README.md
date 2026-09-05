# 🛸 Mission Control Autopilot

Kostenloses, vollautomatisches Dashboard für @spacefactswow:
GitHub holt **jeden Morgen um ca. 6:30 Uhr** selbst die Follower-Zahlen von
TikTok, YouTube und Instagram und dein Dashboard-Link auf dem Handy zeigt sie an.
Kein Abo, kein Server, keine laufenden Kosten.

## Die 3 Dateien

| Datei | Zweck |
|---|---|
| `update.py` | Holt die Zahlen von den öffentlichen Profilseiten (mit Ersatzweg über r.jina.ai, falls eine Seite blockt) |
| `.github/workflows/update.yml` | Startet `update.py` automatisch jeden Tag um 04:30 UTC (= 6:30 dt. Sommerzeit) |
| `docs/index.html` | Dein Dashboard (Mission 10k, Plattform-Karten, Verlauf) – liest `docs/data.json` |

## Einrichtung (einmalig, ca. 15–20 Min.)

1. **GitHub-Account** anlegen: github.com → Sign up (kostenlos).
2. **Neues Repository**: Plus-Symbol → *New repository* → Name z. B. `mission-control` → **Public** → *Create repository*.
3. **Die 3 Dateien anlegen** – jeweils über *Add file → Create new file*:
   - Dateiname `update.py` → Inhalt aus der Datei `update.py` einfügen → *Commit changes*
   - Dateiname `.github/workflows/update.yml` (genau so mit Punkten und Schrägstrichen tippen – GitHub legt die Ordner automatisch an) → Inhalt einfügen → *Commit changes*
   - Dateiname `docs/index.html` → Inhalt einfügen → *Commit changes*
4. **Handles prüfen**: Oben in `update.py` stehen deine Account-Namen.
   TikTok ist schon auf `spacefactswow` gesetzt – trage bei `youtube` und
   `instagram` deine Namen ein (ohne @). Instagram leer lassen = überspringen.
5. **Ersten Lauf starten**: Reiter *Actions* → links „Zahlen aktualisieren" →
   *Run workflow* → grüner Haken nach ~1 Min. = Zahlen sind da.
   (Falls GitHub fragt, ob Workflows erlaubt werden sollen: bestätigen.)
6. **Dashboard veröffentlichen**: *Settings → Pages* → Source: *Deploy from a branch* →
   Branch `main`, Ordner `/docs` → *Save*. Nach 1–2 Min. ist dein Dashboard unter
   `https://DEINNAME.github.io/mission-control/` erreichbar.
7. **Aufs Handy**: Link in Chrome öffnen → Menü (⋮) → **„Zum Startbildschirm hinzufügen"**.
   Ab jetzt: Icon antippen, Zahlen sind aktuell. Fertig.

## Gut zu wissen

- **TikTok-Gesamt-Views** zeigt TikTok nicht öffentlich. Für die 100k-Views-Bar
  trägst du sie 1×/Woche direkt im Dashboard ein (Kästchen „TikTok-Views eintragen",
  Zahl aus TikTok Studio → Analytics). Alles andere läuft automatisch.
- **Falls ein Abruf mal scheitert** (Plattformen blocken Bots gelegentlich):
  Das Skript versucht automatisch einen zweiten Weg. Klappt beides nicht, bleibt
  der letzte Stand mit Datum sichtbar („Stand …") – am nächsten Morgen wird's
  erneut versucht. Nichts geht kaputt.
- **Uhrzeit ändern**: In `update.yml` die Zeile `cron: "30 4 * * *"` anpassen
  (UTC-Zeit; 04:30 UTC = 06:30 deutsche Sommerzeit).
- **Zahlen sofort aktualisieren**: Actions → „Zahlen aktualisieren" → *Run workflow*.
- Das Dashboard zeigt nur öffentliche Zahlen deiner eigenen Accounts, 1 Abruf pro Tag.

## Für Entwickler und Claude

`docs/data.json` schreibt der Bot aus `update.yml` direkt auf main. Nicht von Hand ändern,
Korrekturen laufen über einen kurzen PR (Skill `/data-repair`).

```
python3 -m py_compile update.py                  # Syntax
python3 -m unittest discover -s tests -v         # Tests
python3 tools/check_data.py                      # Schema von data.json
python3 tools/check_html.py                      # Dashboard-Struktur und IDs
python3 tools/stats.py --days 30                 # Zahlen für Berichte
cd docs && python3 -m http.server 8000           # Dashboard lokal ansehen
```

Nur Standardbibliothek, kein Build-Step. Projektregeln in `CLAUDE.md`, Spickzettel in `.claude/CHEATSHEET.md`.
