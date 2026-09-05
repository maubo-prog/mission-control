---
name: pr
description: Bringt die Aenderungen dieser Session sauber auf einen claude/-Branch: Checks, Commit auf Deutsch, Push und Pull Request gegen main. Nur auf ausdruecklichen Aufruf, merged nie.
disable-model-invocation: true
allowed-tools: Read, Grep, Bash
---
# Pull Request vorbereiten

## Ablauf

1. Branch pruefen: `git branch --show-current`. Beginnt er nicht mit `claude/`, dann
   `git fetch origin main` und `git switch -c claude/<thema> origin/main`.
   Niemals auf main committen oder pushen.
2. Passende Checks laufen lassen, alle muessen gruen sein:
   - immer: `python3 -m py_compile update.py`, `python3 -m unittest discover -s tests -v`
   - immer: `python3 tools/check_data.py`, `python3 tools/check_html.py`
   - bei Aenderung an `docs/index.html` zusaetzlich `/dashboard-preview`
3. Diff auf Versehen pruefen: `git diff --stat main`. Tauchen `docs/data.json`, `HANDLES` in
   `update.py` oder `.github/workflows/update.yml` auf, obwohl das nicht die Aufgabe war:
   anhalten und fragen, nicht selbst zuruecksetzen.
4. Commit auf Deutsch, du-Form, knapp: `Fix: ...`, `Setup: ...`, `Doku: ...`.
   Mehrere Themen in mehrere Commits aufteilen.
5. `git push -u origin <branch>`. Bei Netzfehlern bis zu vier Versuche mit Wartezeit.
6. PR gegen main erstellen, Titel deutsch, Body nach `.github/pull_request_template.md`:
   - Web: GitHub-MCP-Tool `create_pull_request`
   - CLI: `gh pr create --base main --title "..." --body "..."`
7. PR-Link im Chat nennen und `/handoff` vorschlagen.

## Regeln

- Nie mergen, nie auf main pushen, nie force-pushen. Der Merge ist Sache des Betreibers.
- Der PR bleibt klein. Passt die Aenderung nicht in einen Satz, ist es mehr als ein PR.
- Im PR-Body ehrlich eintragen, welche Checks tatsaechlich liefen und welche nicht.
