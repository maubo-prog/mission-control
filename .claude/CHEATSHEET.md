# Spickzettel

Nur fuer dich, wird nicht automatisch geladen. Alles hier kostet nichts extra, ausser wo es dabeisteht.

## Modell und Aufwand

- `sonnet` fuer den Alltag, `/model opus` oder `/model opusplan` (Opus plant, Sonnet setzt um) fuer Umbauten,
  `haiku` fuer reine Nachfragen, `best` nur fuer die schwersten Aufgaben.
- Standardmodell ist auf Pro `sonnet`, auf Max `opus`. Mitten in der Session nicht wechseln, der Cache geht verloren.
- Aufwand: Standard ist `high`. `/effort medium` fuer Routine, `xhigh` nur fuer harte Fehler.
- Auf dem Web `/model` und `/effort` mit Argument aufrufen, also `/model sonnet` statt nur `/model`.

## Sessions

- Eine Aufgabe pro Session. Start `/briefing`, Ende `/handoff`.
- Danach CLI: `/clear`. Web: neue Session aus der Seitenleiste, beim Anlegen denselben `claude/`-Branch waehlen,
  solange der PR nicht gemergt ist.
- Bei langem Verlauf `/kompakt`, danach `/compact <fokus>`. Vorher `/context` anschauen, beides geht auch auf dem Web.
- Fortsetzen: CLI `claude --continue` oder `/resume`. Web: alte Session in der Seitenleiste oeffnen,
  dort gibt es kein `/resume` und kein `/clear`.

## Wenn das Limit naht

- Erst `/compact`, dann `haiku`, dann Pause. `/fast` nie, das kostet mehr und bringt hier nichts.
- `/usage` woechentlich, `/doctor` nach Setup-Aenderungen, `/insights` monatlich (nur CLI).

## Modus und Rechte

- Modus wechseln: Shift+Tab in der CLI, Modus-Waehler auf dem Web. Auto, acceptEdits, Plan.
- `/permissions` zeigt die aktiven Regeln. Die Projektregeln stehen in `.claude/settings.json`.
- Nach ein paar Sessions `/fewer-permission-prompts` laufen lassen, das erweitert die Allowlist aus echten Transkripten.
- `/mcp`: fuer dieses Repo nur GitHub verbunden lassen, den Rest abschalten.

## Opt-in, bewusst nicht aktiv

- `/plugin install security-guidance@claude-plugins-official`
  Haengt Hooks an SessionStart, UserPromptSubmit, PostToolUse und Stop und startet nach jedem Zug mit
  Dateiaenderung und bei jedem Commit einen zusaetzlichen Opus-Review-Aufruf, der auf dein Kontingent zaehlt.
  Hier reicht `/security-review` vor dem PR.

## Lokal einmalig ausfuehren (nur CLI)

```
/plugin install github@claude-plugins-official          # GitHub-MCP fuer die CLI
/plugin install commit-commands@claude-plugins-official # optional, /pr deckt das meiste ab
/reload-plugins
/plugin marketplace add anthropics/knowledge-work-plugins
/install-github-app          # nur wenn du @claude-Reviews im PR willst, braucht gh
/web-setup                   # wenn Cloud-Sessions GitHub ueber dein gh-Token brauchen
/statusline                  # Statuszeile mit Modell, Kontext-Prozent und Kosten
/doctor                      # einmal nach dem Setup
```

## Wiederkehrende Befehle im Repo

```
python3 tools/stats.py --days 30     # Zahlen, nie data.json lesen
python3 tools/check_data.py --today  # hat der Bot heute geliefert
cd docs && python3 -m http.server 8000
```
