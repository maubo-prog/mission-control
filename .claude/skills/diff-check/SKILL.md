---
name: diff-check
description: Prueft einen Diff oder Pull Request gegen die Invarianten aus CLAUDE.md und meldet maximal sieben Befunde nach Schwere. Aendert nichts. Nutzen bei "schau drueber", "pruef den Diff", vor jedem Merge.
allowed-tools: Read, Grep, Glob, Bash, Agent
---
# Diff pruefen

## Ablauf

1. Diff holen:
   - lokal: `git diff main...HEAD --stat`, danach `git diff main...HEAD`
   - zu einer PR-Nummer: Web ueber das GitHub-MCP-Tool, CLI ueber `gh pr diff <nr>`
2. Ist der Diff laenger als 200 Zeilen: an den Agent `pruefer` geben und nur dessen Ergebnis
   uebernehmen. Den vollen Diff nicht in den Hauptkontext holen.
3. Gegen diese Punkte pruefen, in dieser Reihenfolge:
   - Schema: bleiben `date`, `tiktok.f/l`, `youtube.f/v`, `instagram.f` unveraendert? Werte int oder null?
   - `merge()`: ueberschreibt null weiterhin keinen guten alten Wert?
   - Abhaengigkeiten: nur Standardbibliothek, kein Build-Step, kein Framework?
   - `docs/index.html`: globale Handler `setMetric`, `toggleAll`, `saveManual` noch global? IDs noch vorhanden?
   - Workflows: minimale `permissions`, `timeout-minutes`, Actions auf Major-Tags? `update.yml` unberuehrt?
   - Versehen: `docs/data.json`, `HANDLES` oder die Cron-Zeit mitgeaendert?
   - Sprache: Texte und Commit-Message deutsch, Bezeichner englisch?
   - Oeffentlichkeit: nichts Privates unter `docs/`, keine Secrets im Diff?
4. Befunde sortieren: erst was bricht, dann was riskant ist, dann Kosmetik.

## Ausgabe

Maximal sieben Zeilen, je eine pro Befund, im Format
`<Schwere>: <Datei>:<Zeile> <was ist falsch> <konkreter Vorschlag>`.
Nichts gefunden: eine Zeile, die das sagt. Keine Datei aendern, kein Commit.

Fuer den allgemeinen Bug-Blick zusaetzlich den eingebauten `/code-review` laufen lassen.
