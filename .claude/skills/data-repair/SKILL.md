---
name: data-repair
description: Korrigiert einen einzelnen Eintrag in docs/data.json per Skript statt per Editor und bringt die Korrektur schnell ueber einen PR nach main. Nur auf ausdruecklichen Aufruf, etwa bei falschen Werten oder einem Issue mit Label zahlen.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---
# Daten korrigieren

`docs/data.json` gehoert dem Bot. Jede Handkorrektur ist ein Wettlauf gegen den naechsten
Lauf um 04:30 UTC, deshalb: klein halten, schnell mergen lassen.

## Ablauf

1. Ausgangslage pruefen: `python3 tools/stats.py --days 14`. Die Datei nicht mit Read oeffnen.
2. Branch anlegen: `git fetch origin main` und `git switch -c claude/fix-daten-<datum> origin/main`.
   Nur so beginnt die Korrektur auf dem aktuellen Bot-Stand.
3. Aenderung per kurzem Python-Skript, nie per Editor. Muster:
   `python3 -c "import json,pathlib;p=pathlib.Path('docs/data.json');d=json.loads(p.read_text());[e['instagram'].update({'f':210}) for e in d['entries'] if e['date']=='2026-09-01'];p.write_text(json.dumps(d,ensure_ascii=False,indent=1))"`
   (fragt nach Erlaubnis). Formatierung genau wie `update.py` sie schreibt: `indent=1`,
   `ensure_ascii=False`.
4. Nur vorhandene Schluessel setzen: `tiktok.f`, `tiktok.l`, `youtube.f`, `youtube.v`, `instagram.f`.
   Werte sind int oder null, nie String, nie 0 als Ersatz fuer null.
5. Pruefen: `python3 tools/check_data.py`, danach `git diff --stat` (es darf nur eine Datei
   und nur der erwartete Eintrag betroffen sein).
6. Commit `Fix: Daten <datum> korrigiert`, dann `/pr`. Im PR dazuschreiben, dass er schnell
   gemergt werden sollte. Bei Konflikt mit einem neuen Bot-Commit: auf main rebasen, nicht
   die Bot-Werte ueberschreiben.

## Sonderfaelle

- **Instagram aus einem Issue "Zahlen nachtragen"**: die gemeldete Zahl als `instagram.f`
  beim gemeldeten Datum eintragen. Issue danach schliessen und darin nennen, was eingetragen wurde.
- **TikTok-Gesamtviews**: noch nicht speicherbar. `series()` in `docs/index.html` setzt
  `tiktok.v` fest auf null und liest den Wert nur aus dem localStorage. Erst wenn `series()`
  `e.tiktok.v` aus `data.json` liest, darf der Schluessel dort befuellt werden. Bis dahin im
  Bericht als "noch nicht speicherbar" vermerken, den Wert nicht heimlich ablegen.
- **Ausreisser statt Fehler**: wenn unklar ist, ob ein Wert falsch oder nur ungewoehnlich ist,
  nichts aendern und nachfragen.
