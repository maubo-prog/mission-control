# Session-Uebergabe

Wird zu jedem Sessionstart geladen (Import in `CLAUDE.md`). Liegt auf dem `claude/`-Branch und ist
auf main erst nach dem Merge sichtbar, bis dahin naechste Web-Session auf denselben Branch stellen.
Schreiben nur ueber `/handoff` (ersetzt den Inhalt, haengt nichts an). Maximal 40 Zeilen.

## Erledigt

- Setup fuer Claude Code angelegt: `CLAUDE.md`, `.claude/rules/` (3), `.claude/settings.json`,
  `.claude/hooks/` (3), `.claude/skills/` (9), `.claude/agents/pruefer.md`, `CHEATSHEET.md`, `routines.md`.
- Hilfsskripte `tools/check_data.py`, `check_html.py`, `stats.py`, nur Standardbibliothek.
- Tests `tests/test_update.py` (7 Faelle zu `compact`, `merge`, `grab`), kein Netzzugriff.
- GitHub: `ci.yml`, `watchdog.yml` (Ausfall-Alarm, kostenlos, legt Issue an), `dependabot.yml`,
  `pull_request_template.md`, `ISSUE_TEMPLATE/zahlen.yml`, `.gitignore`, README-Abschnitt.

## Offen

- Manuelle Schritte stehen im Abschlussbericht: Ordner als vertrauenswuerdig bestaetigen,
  Branch-Schutz Variante A auf main, Label `zahlen`, lokale CLI-Befehle aus dem Spickzettel.
- Nicht angefasst: YouTube-Views falsch, Instagram null, TikTok-Likes gerundet. Fixes ueber `/scraper-fix`.
- Manuell noch offen: Branch-Schutz Variante A auf main, Label `zahlen`, lokale CLI-Befehle.

## Naechster Schritt

- PR mergen, dann neue Session mit `/briefing`. Erste echte Aufgabe: `/scraper-fix` fuer die
  YouTube-Views, das ist die einzige durchgaengig falsche Zahl.

## Geprueft

- `py_compile update.py` OK, `unittest discover -s tests` 7 Tests OK.
- `tools/check_data.py` OK (43 Eintraege), `tools/check_html.py` OK (7 IDs), `tools/stats.py` OK (23 Zeilen).
- `json.tool .claude/settings.json` OK, `bash -n` auf alle drei Hooks OK.
- 10 Hook-Simulationen mit erwarteten Exit-Codes, dazu ein Live-Test: `check.sh` fing eine kaputte
  Python-Datei mit Exit 2 ab. YAML aller vier neuen Dateien mit `yaml.safe_load` OK.
- `git diff main --stat`: `update.py`, `update.yml`, `docs/data.json` unveraendert.

## Branch und offene PRs

- Branch: claude/setup-repo-claude-code-bm1zhu, frisch von main nach dem Merge von PR 2
- Das Setup liegt auf main. Folge-PR entfernt `enabledPlugins`, der Skill `/pr` deckt das ab.
