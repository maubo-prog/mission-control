---
name: briefing
description: Laedt zu Beginn einer Session nur das, was fuer die anstehende Aufgabe wirklich noetig ist, und fasst den Stand in zehn Zeilen zusammen. Nutzen bei Sessionstart, "leg los mit ...", "was ist der Stand".
allowed-tools: Read, Grep, Glob, Bash, Agent
---
# Briefing

Ziel: mit so wenig Kontext wie moeglich arbeitsfaehig werden. Keine Datei ins Fenster holen,
die fuer die konkrete Aufgabe nicht gebraucht wird.

## Ablauf

1. `.claude/handoff.md` ist ueber den Import in `CLAUDE.md` schon geladen. Nicht erneut lesen.
2. Lage holen, mehr nicht:
   - `git branch --show-current`
   - `git status --short`
   - `git log --oneline -5`
3. Aufgabe einordnen und nur die passende Datei oeffnen:
   - Zahlen, Abruf, Ausfall: `update.py`, plus `python3 tools/stats.py --days 7`
   - Dashboard, Darstellung: `docs/index.html`
   - CI, Workflow, Alarm: die betroffene Datei unter `.github/workflows/`
   - Nur eine Frage zum Stand: gar keine Datei oeffnen
4. Wenn unklar ist, wo etwas steht: Suche an den Explore-Subagenten geben, nicht selbst
   mehrere Dateien lesen. Nur das Ergebnis kommt zurueck.
5. `docs/data.json` nie oeffnen. Zahlen ausschliesslich ueber `python3 tools/stats.py`.

## Ausgabe

Genau ein Lagebericht, maximal zehn Zeilen:

- Branch und ob der Arbeitsbaum sauber ist
- letzte drei Commits in einer Zeile
- offene Punkte aus der Uebergabe
- was du als naechsten Schritt vorschlaegst
- welche Dateien du dafuer geoeffnet hast

Danach warten. Nicht ungefragt mit der Umsetzung anfangen.
