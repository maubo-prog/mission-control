# Claude-Code-Setup-Prompt für maubo-prog

Stand: 2026-09-04. Alle Slash-Befehle, Settings-Keys, Hook-Felder, Frontmatter-Felder, Plugin- und Marketplace-Namen wurden gegen die offizielle Doku (code.claude.com/docs) und Claude Code 2.1.260 geprüft; die Hook-Skripte aus Teil A wurden gegen dieses Repo simuliert. Stellen, die sich nur in deiner Umgebung prüfen lassen, sind mit "(bitte prüfen: ...)" markiert.

Inhalt:
1. Teil A: Setup-Auftrag für `mission-control`. In eine neue Claude-Code-Session kopieren (Web oder CLI).
2. Teil B: Setup-Auftrag für den Videoproduktionsordner. Optional, CLI auf dem Windows-Rechner, nach Teil A.
3. Teil C: Vorschläge über das Setup hinaus und Entscheidungen, die bei dir liegen.

---

# Teil A: Setup-Auftrag für `mission-control`

## So benutzt du diesen Prompt

Kopiere alles ab "Deine Rolle" in eine neue Session von Claude Code auf dem Web (claude.ai/code, Repo `maubo-prog/mission-control`) oder in die CLI im Repo-Ordner (`claude --model opus`). Modell für diese eine Session: `opus` (oder `best`, das neueste Fable-Modell); Modus: Auto (auf Pro und Max der Standard) oder Accept edits, kein Plan-Modus, der Prompt ist der Plan. Auf dem Web wählst du Modell und Modus beim Anlegen der Session. Am Ende bekommst du einen Pull Request und einen Bericht mit den Schritten, die nur du selbst erledigen kannst (Repo-Einstellungen, GitHub-App, Plugins im claude.ai-Katalog). Rechne mit einer langen Session; wenn der Kontext eng wird, `/compact Setup-Auftrag: Phase, angelegte Dateien, offene Punkte behalten`.

---

## Deine Rolle und das Ziel

Du bist ein erfahrener Senior-Engineer und richtest ein sehr kleines Repository (5 Dateien, Solo-Betreiber, kein Build, keine Abhängigkeiten) für die Arbeit mit Claude Code ein. Ich bin Content-Creator, kein Berufsentwickler, und will künftig mit möglichst wenigen Rückfragen, wenig Kontextverbrauch und ohne Unterbrechungen durch Limits arbeiten, sowohl in Claude Code auf dem Web als auch in der CLI. Motto: solide und schlank. Lieber die 20 % Konfiguration, die 80 % bringen, als ein Setup, das mehr Token frisst als es spart.

## Arbeitsregeln (gelten für die ganze Session)

1. Erst analysieren, dann in kleinen, einzeln geprüften Schritten arbeiten. Nach jeder Phase kurz berichten: was angelegt, was geprüft, was offen.
2. Nie auf `main` pushen, nie `main` direkt ändern. Bleib auf dem aktuellen Branch, falls er mit `claude/` beginnt (Web-Sessions sind an ihren Branch gebunden); sonst lege `claude/setup` von `main` an. Push auf diesen Branch und PR-Erstellung darfst du machen, das Mergen mache ich.
3. `.github/workflows/update.yml` (täglicher Bot), `update.py` und `docs/data.json` bleiben in dieser Session unverändert. Keine neuen Abhängigkeiten, kein Build-Step, kein Framework.
4. Vor allem, was Geld kostet (API-Keys, bezahlte Plugins, Routinen, die täglich Kontingent verbrauchen), Secrets braucht oder destruktiv ist (Dateien löschen, Force-Push, Repo-Einstellungen), anhalten und fragen. Alles andere machst du eigenständig.
5. Alles, was du in dieser Umgebung nicht selbst tun kannst (Slash-Befehle wie `/plugin`, `/permissions`, `/context`, Dateien unter `~/.claude/`, GitHub-Repo-Settings, claude.ai-Plugin-Katalog), schreibst du als nummerierte Anleitung mit exakten Befehlen in den Bericht, statt es zu behaupten. Auf dem Web kannst du nur Dateien im Repo anlegen.
6. Sprache: Antworten, Kommentare, Commit-Messages, Skill-Texte auf Deutsch (du-Form), Code-Bezeichner Englisch. Keine Gedankenstriche, keine Emojis.
7. Jede Datei, die in jeder Session geladen wird (CLAUDE.md, handoff.md, Skill-Beschreibungen), hat ein Zeilenbudget. Halte es ein oder begründe die Überschreitung.
8. Wenn du bei einem Befehl, Settings-Key oder Feature unsicher bist, markiere es im Bericht mit "(bitte prüfen: ...)" statt es als Fakt hinzustellen.
9. Offene Fragen an mich sammelst du (maximal 5) für den Abschlussbericht und arbeitest mit sinnvollen Annahmen weiter, statt mitten in der Session zu blockieren.

## Kontext, den du als gegeben nehmen kannst

- Repo `maubo-prog/mission-control`, Default-Branch `main`, GitHub Pages aus `/docs` (öffentlich). Dashboard für den Creator-Account `@spacefactswow` (TikTok, YouTube Shorts, Instagram Reels). Mission: 10.000 TikTok-Follower und 100k Views in 30 Tagen.
- Dateien: `README.md` (Anleitung für Nicht-Entwickler), `update.py` (Python 3.12, nur Standardbibliothek; `HANDLES` oben, `compact()`, `grab(patterns, text)`, `get_tiktok/get_youtube/get_instagram`, `merge()`, `main()` hinter `if __name__ == "__main__"`, also gefahrlos importierbar), `.github/workflows/update.yml` (Cron `30 4 * * *` UTC + `workflow_dispatch`, `contents: write`, committet `docs/data.json` als `Stats YYYY-MM-DD` direkt auf `main`), `docs/index.html` (Ein-Datei-Dashboard, Vanilla JS, manuelle Werte nur im localStorage des Handys; liest `tiktok.v` heute nur aus localStorage, nicht aus data.json), `docs/data.json` (rund 40 Einträge seit 2026-07-24, plus einer pro Tag; Schema `{updated, handles, entries:[{date, tiktok:{f,l}, youtube:{f,v}, instagram:{f}}]}`, Werte int oder null).
- Bekannte Schwächen (nur dokumentieren, in dieser Session nicht fixen): YouTube-Views falsch (Regex greift ein einzelnes Video), Instagram immer null, TikTok-Likes seit 12.08. auf 100er gerundet, TikTok-Ausfälle am 23.08. und 28.08. ohne Alarm, kein `.gitignore`, keine Tests.
- Vorhandene Claude-Konfiguration im Repo: keine. Kein `CLAUDE.md`, keine Skills, keine Hooks. Eine `.claude/settings.local.json` kann von der Web-Umgebung angelegt sein; sie ist global git-ignoriert und bleibt unangetastet.
- Sandbox hat Python 3.11, aber kein `gh`; CI nutzt Python 3.12. Keine 3.12-only-Syntax. GitHub-Aktionen laufen auf dem Web über die GitHub-MCP-Tools (in meinen Web-Sessions ist der GitHub-MCP-Server verbunden, prüfe das mit `/mcp` oder an der Tool-Liste), in der CLI über `gh`.
- Auf Konto-Ebene (claude.ai, in jeder Session synchronisiert) habe ich vier eigene Skills für die Videoproduktion: `spacefacts-produktionsauftrag` (kompletter Produktionslauf von der Themenwahl bis zum Uploadplan), `spacefacts-motion-graphics` (SpaceMotion-Engine, Renderpipeline), `konkurrenz-video-forensik` (Videoanalyse im eingebauten Browser und offline mit OpenCV und ffmpeg) und `spacefacts-cover-design` (Cover, Thumbnails, Banner). Sie gehören zum zweiten Projekt, dem Produktionsordner `C:\Users\mauri\OneDrive\Tiktok\` auf meinem Windows-Rechner, der nicht auf GitHub liegt und in dem täglich automatisierte Aufgaben laufen. In dieser Session nicht anfassen, keine Projekt-Skills mit gleichem oder ähnlichem Namen anlegen. In CLAUDE.md nur eine Zeile Verweis: gleiche Marke wie das Dashboard (Gelb #FFEC00 auf Tiefblau, Montserrat), Videoarbeit läuft über diese Konto-Skills und einen eigenen Auftrag (Teil B).

---

## Phase 0: Bestandsaufnahme (nur lesen)

Tu das:
- `git status`, `git branch --show-current`, `git log --oneline -5`, `ls -la .claude .github/workflows docs`, `cat .claude/settings.local.json`.
- `python3 -m py_compile update.py && python3 -m json.tool docs/data.json > /dev/null && echo OK`.
- `docs/data.json` nie mit dem Read-Tool öffnen. Stattdessen einmalig: `python3 -c "import json;d=json.load(open('docs/data.json'));e=d['entries'];print(d['updated'],len(e));print(e[0]);print(e[-1])"` (fragt im manuellen Modus einmal nach, das ist so gewollt; ab Phase 2 übernimmt `tools/stats.py`).
- Lies `README.md`, `update.py`, `update.yml` und `docs/index.html` einmal komplett (zusammen ca. 650 Zeilen); danach nur noch gezielt per Grep.

Prüfen: alle Befehle laufen ohne Fehler. Bericht: 5 Zeilen, was existiert, was fehlt, welcher Branch.

---

## Phase 1: `CLAUDE.md`, pfadgebundene Regeln, `handoff.md`

Budget `CLAUDE.md`: 80 bis 120 Zeilen, unter 6 KB. Nur, was Claude nicht aus dem Code ableiten kann. Kein README-Duplikat, kein `@`-Import der README (kostet jede Session Token ohne Nutzen).

```
# Mission Control Autopilot        (1 Zeile: was, für wen, Ziel 10k/100k, kostenlos, serverlos)
## Sprache                          (Deutsch du-Form für Text, Commits, UI; Code-Bezeichner Englisch)
## Dateien                          (5 Einträge, je 1 Zeile: Rolle der Datei, nicht ihr Inhalt; docs/ ist öffentlich)
## Befehle                          (py_compile, json.tool, unittest, tools/check_data.py, tools/check_html.py, tools/stats.py, http.server für docs/; Warnung vor `python3 update.py`: echte Netzabrufe, überschreibt den heutigen Eintrag, danach `git checkout docs/data.json`)
## Datenschema docs/data.json       (Schlüssel f/l/v, int oder null, eindeutig pro Datum, sortiert, max. 400; index.html hängt an genau diesen Schlüsseln; `tiktok.v` ist als optionaler Schlüssel geplant, wird vom Dashboard aber noch nicht gelesen)
## Invarianten                      (merge(): null überschreibt nie gute Werte; stdlib only; Workflow braucht nur contents: write)
## Nicht anfassen ohne Rückfrage    (data.json per Hand auf main, HANDLES, Cron-Zeit, docs/ als Pages-Root, update.yml)
## Bekannte Schwächen (Stand 2026-09-04)   (YouTube-Views, Instagram null, Likes gerundet, Ausfälle ohne Alarm, localStorage)
## Arbeitsweise                     (Branch claude/<thema>, kleine PRs, Commit-Stil 'Fix: ...' / 'Setup: ...', vor Commit die Checks; Erkundung an Explore-Subagent, lange Diffs an Agent pruefer)
## Kontext-Hygiene                  (max. 10 Zeilen, Inhalt aus Phase 7)
## Zeit                             (Cron UTC = 06:30 MESZ / 05:30 MEZ, oft 10 bis 40 Min. verspätet; Datum = Runner-Datum UTC)
## Session-Übergabe
@.claude/handoff.md
```

Der `@`-Import lädt `.claude/handoff.md` automatisch zum Sessionstart. Lege die Datei mit Platzhalter an (max. 40 Zeilen, Abschnitte Erledigt / Offen / Nächster Schritt / Geprüfte Befehle / Branch und offene PRs). Sie wird committet, nie ignoriert: auf dem Web startet jede Session aus einem frischen Checkout, nur so überlebt die Übergabe. Wichtig, und so auch in die Datei schreiben: die Übergabe liegt auf dem `claude/`-Branch und ist auf `main` erst nach dem Merge des PR sichtbar; bis dahin starte ich die nächste Session auf demselben Branch (Branch-Wahl beim Anlegen der Web-Session).

Pfadgebundene Regeln in `.claude/rules/` (Frontmatter `paths:`; laden nur, wenn passende Dateien bearbeitet werden), je maximal 15 Zeilen:
- `scraper.md` (`paths: ["update.py", "tests/**"]`): Parsen vom Laden trennen, wenn umgebaut wird; Regex nur als Fallback; jede Änderung mit Fixture-Test; Exceptions nicht still schlucken.
- `dashboard.md` (`paths: ["docs/index.html"]`): innerHTML-Aufbau und globale Handler `setMetric/toggleAll/saveManual` beibehalten, keine Module, Viewport 390px, `lang="de"`, Änderungen nur mit `/dashboard-preview` committen.
- `workflows.md` (`paths: [".github/workflows/**"]`): `update.yml` nicht ändern; neue Workflows mit minimalen `permissions`, `timeout-minutes`, `concurrency`; Actions auf Major-Tags (`@v4`, `@v5`), Dependabot hält sie aktuell.

Prüfen: `wc -l CLAUDE.md .claude/handoff.md .claude/rules/*.md` innerhalb der Budgets; jede Zeile hat einen konkreten Fakt. Bericht: Zeilenzahlen, was du bewusst weggelassen hast.

---

## Phase 2: Hilfsskripte, `.claude/settings.json`, Hooks, `.gitignore`

### 2a Hilfsskripte in `tools/` (reine Standardbibliothek, laufen unter Python 3.11 und 3.12)

Das sind Projektskripte, keine Claude-Code-Features. Hooks, CI und Skills rufen dieselben Skripte auf, damit nichts doppelt gepflegt wird.
- `tools/check_data.py`: lädt `docs/data.json`; prüft gültiges JSON, Pflichtschlüssel (`tiktok.f/l`, `youtube.f/v`, `instagram.f`), Datum eindeutig und aufsteigend, Werte int oder null, max. 400 Einträge. Zusätzliche optionale Schlüssel (z. B. später `tiktok.v`) sind erlaubt, damit die spätere Erweiterung den Hook nicht bricht. Option `--today`: zusätzlich Exit 1, wenn der letzte Eintrag nicht das heutige UTC-Datum trägt oder `tiktok.f` null ist. Ausgabe eine Zeile, Exit 1 bei Fehler.
- `tools/check_html.py`: prüft `docs/index.html` ohne Node: `html.parser` läuft durch, `<script>`-Tags balanciert, `lang="de"` vorhanden, jede per `getElementById("...")` referenzierte ID kommt als `id="..."` oder `id='...'` im Markup vor (Regex `getElementById\("(\w+)"\)`; auf dem aktuellen Stand sind das 7 IDs, alle vorhanden). Exit 1 bei Fehler.
- `tools/stats.py`: die einzige Art, wie Berichte an die Zahlen kommen. Optionen `--days N` (Standard 30) und `--json`. Ausgabe maximal 40 Zeilen: letzter Stand je Plattform, Delta 7 und 30 Tage, Tempo pro Tag, Prognosedatum für 10k TikTok-Follower (linear gesamt und auf Basis der letzten 14 Tage), beste und schwächste Tage, Liste der null-Tage. YouTube-Views als "unzuverlässig" markieren.

### 2b `.claude/settings.json` (geteilt, wird committet)

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 -m py_compile:*)", "Bash(python3 -m json.tool:*)",
      "Bash(python3 -m unittest:*)", "Bash(python3 -m http.server:*)",
      "Bash(python3 tools/*)", "Bash(bash .claude/hooks/*)", "Bash(chmod +x .claude/hooks/*)",
      "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)", "Bash(git branch:*)", "Bash(git fetch:*)",
      "Bash(git add:*)", "Bash(git commit:*)", "Bash(git checkout -b:*)", "Bash(git switch -c:*)",
      "Bash(git checkout docs/data.json)",
      "Bash(git push -u origin claude/*)", "Bash(git push origin claude/*)",
      "Bash(ls:*)", "Bash(wc:*)", "Bash(head:*)", "Bash(tail:*)",
      "Bash(gh pr view:*)", "Bash(gh pr diff:*)", "Bash(gh pr create:*)", "Bash(gh run view:*)", "Bash(gh run list:*)",
      "WebFetch(domain:code.claude.com)"
    ],
    "ask": [
      "Bash(python3 update.py:*)", "Bash(python update.py:*)", "Bash(python3 -c:*)",
      "Bash(gh pr merge:*)", "Bash(gh workflow run:*)", "Bash(gh api:*)", "Bash(gh secret:*)",
      "mcp__github__push_files", "mcp__github__create_or_update_file", "mcp__github__delete_file"
    ],
    "deny": [
      "Bash(git push origin main:*)", "Bash(git push --force:*)", "Bash(git push -f:*)",
      "Bash(git reset --hard*)", "Bash(rm -r*)", "Bash(rm -f*)",
      "Read(/docs/data.json)",
      "mcp__github__merge_pull_request"
    ]
  },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard.sh\"", "timeout": 10 } ] }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write", "hooks": [ { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/check.sh\"", "timeout": 30 } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/stop.sh\"", "timeout": 10 } ] }
    ]
  }
}
```

Dazu:
- Kein `defaultMode` in der Datei. Auf Pro und Max startet jede Session im Auto-Modus (ein Klassifikator entscheidet, die wenigsten Rückfragen); ein `defaultMode: acceptEdits` würde das überschreiben und jeden Bash-Befehl außerhalb der Allowlist wieder fragen lassen. `auto` und `bypassPermissions` greifen aus Projekt-Settings ohnehin nicht (nur aus `~/.claude/settings.json` oder Managed Settings). Die Allowlist ist für den manuellen Modus und für den Fall, dass der Klassifikator zögert; `allow`-Regeln aus der Projektdatei gelten erst, nachdem ich den Ordner einmal als vertrauenswürdig bestätigt habe, `deny` und `ask` sofort. `.claude/settings.json` wird auch in Web-Sessions gelesen, weil die Datei im Checkout liegt; `~/.claude/settings.json` und `settings.local.json` dort nicht. Web-Sessions genehmigen Dateiänderungen immer automatisch, dort zählen nur die Bash-Regeln.
- Wildcard-Regeln: `Bash(git commit:*)` ist dasselbe wie `Bash(git commit *)`, also Präfix plus Leerzeichen plus Rest. Das Leerzeichen gehört zur Regel: `Bash(ls *)` passt nicht auf `lsof`. Deshalb stehen Pfad-Präfixe ohne Leerzeichen als `Bash(python3 tools/*)` und `Bash(git push origin claude/*)`; ein `Bash(python3 tools/:*)` würde `python3 tools/stats.py` nie treffen. `:*` nur nach ganzen Wörtern verwenden.
- `Read(/docs/data.json)` in `deny` ist Absicht: die Datei wächst täglich und würde jedes Mal Kontext fressen. Der führende `/` verankert den Pfad an der Projektwurzel (relativ zur Settings-Datei), damit die Regel auch nach `cd docs` greift; `./docs/...` wäre relativ zum aktuellen Arbeitsverzeichnis. Zahlen kommen aus `tools/stats.py`, Reparaturen laufen per Skript über `/data-repair`. Erkläre das in CLAUDE.md, damit ich mich nicht wundere.
- `Bash(python3 -c:*)` steht bewusst unter `ask`, nicht unter `allow`: beliebige Python-Einzeiler könnten `update.main()` starten, Dateien löschen oder data.json ausgeben und damit die `ask`/`deny`-Regeln umgehen. Die `tools/`-Skripte ersetzen die Einzeiler. Die `deny`-Liste ist eine Sicherung gegen Versehen, keine Sicherheitsgrenze; `rm -r*` und `rm -f*` fangen auch `rm -rf` und `rm -fr`, andere Schreibweisen nicht. Das eigentliche Netz gegen Push nach main ist `guard.sh`.
- Die `mcp__github__...`-Namen entsprechen dem GitHub-MCP-Server meiner Web-Sessions (dort heißen die Tools genau `push_files`, `create_or_update_file`, `delete_file`, `merge_pull_request`, `create_pull_request`). Das `github`-Plugin der CLI bringt einen eigenen Server mit, dessen Toolnamen abweichen können; nenne im Bericht, welche Namen deine Session tatsächlich zeigt.
- Kein `model`-Key in der committeten Datei: sie gilt auch in Web-Sessions, und ob sie dort die Modellwahl beim Anlegen der Session überschreibt, ist nicht belegt (bitte prüfen). Standardmodell `sonnet` kommt in `~/.claude/settings.json` (Phase 8) bzw. per `/model sonnet`; für Umbauten wechsle ich selbst mit `/model opus` oder `/model opusplan`. Keine Keys eintragen, die du nicht kennst.

### 2c Hook-Skripte in `.claude/hooks/` (ausführbar machen)

Hooks lesen ihren Input als JSON von stdin (`tool_input.file_path` bei Edit/Write, `tool_input.command` bei Bash); wir lesen ihn mit Python statt `jq`, damit die Hooks auch auf meinem Rechner ohne `jq` laufen. `$CLAUDE_PROJECT_DIR` ist der dokumentierte Platzhalter für die Projektwurzel. Hooks unterliegen nicht den Permission-Regeln. PreToolUse: Exit 2 blockiert, stderr ist die Begründung; bei Exit 0 wirkt nur eine JSON-Entscheidung auf stdout. PostToolUse: Exit 2 blockiert nichts mehr, zeigt Claude aber die stderr-Meldung. Stop: immer Exit 0, sonst kann die Session nicht enden; reines stdout landet dort nur im Debug-Log, weder ich noch Claude sehen es. Sichtbar wird eine Notiz nur über das JSON-Feld `systemMessage`.

```bash
#!/usr/bin/env bash
# .claude/hooks/check.sh  (PostToolUse): prüft nur die gerade geänderte Datei, unter 2 s.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
f=$(python3 -c 'import json,sys;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
case "$f" in
  *.py)                      python3 -m py_compile "$f" || exit 2 ;;
  *docs/data.json)           python3 tools/check_data.py || exit 2 ;;
  *docs/index.html)          python3 tools/check_html.py || exit 2 ;;
  *.github/workflows/*.yml)  if python3 -c "import yaml" 2>/dev/null; then
                               python3 -c "import yaml,sys;yaml.safe_load(open(sys.argv[1]))" "$f" || exit 2
                             else echo "Hinweis: PyYAML fehlt, YAML nicht geprüft" >&2; fi ;;
  *.json)                    python3 -m json.tool "$f" > /dev/null || exit 2 ;;
esac
exit 0
```

```bash
#!/usr/bin/env bash
# .claude/hooks/guard.sh  (PreToolUse Bash): sperrt Push nach main und Force-Push, erzwingt Rückfrage vor dem Live-Scraper.
# Exit 2 = Befehl blockieren, stderr ist die Begründung.  Exit 0 = erlauben; dann wirkt nur JSON auf stdout.
cmd=$(python3 -c 'import json,sys;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
ask=0
# Verkettete Befehle (&&, ||, ;) einzeln prüfen und nur am Segmentanfang matchen, damit
# "git push origin claude/x && git log main" und "grep 'import update' tests/..." nicht anschlagen.
while IFS= read -r part; do
  part="${part#"${part%%[![:space:]]*}"}"
  case "$part" in
    "git push"*" main"|"git push"*" main "*|"git push"*":main"*|"git push"*"--force"*|"git push -f"*)
      echo "Gesperrt: Push nach main oder Force-Push. Nutze einen claude/-Branch und einen PR." >&2; exit 2 ;;
    "python3 update.py"*|"python update.py"*|"python3 -c "*"import update"*|"python -c "*"import update"*) ask=1 ;;
  esac
done < <(printf '%s\n' "$cmd" | tr ';&|' '\n')
if [ "$ask" = 1 ]; then
  printf '%s' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"update.py macht echte Netzabrufe und überschreibt den heutigen Eintrag in docs/data.json. Danach git checkout docs/data.json."}}'
fi
exit 0
```

`stop.sh`: `cd "${CLAUDE_PROJECT_DIR:-.}"`; wenn `git status --short` Inhalt hat, genau eine Zeile `{"systemMessage":"Hinweis: uncommittete Änderungen vorhanden. Nur zur Info, nichts weiter tun."}` auf stdout ausgeben, sonst nichts; danach `exit 0`. Kein Testlauf im Stop-Hook: reines stdout sieht niemand, und ein Testergebnis, das Claude zu sehen bekäme, würde nach dem Stop neue Züge auslösen (Endlosschleifen-Risiko). Tests laufen über `check.sh`, `/pr` und die CI. `systemMessage` ist das dokumentierte universelle Feld für Hinweise an den Nutzer; einzelne Events verwerfen es. Falls der Hinweis nach einem Testlauf nicht sichtbar ist, den Stop-Hook ganz entfernen, statt ihn umzubauen.

Bewusst weggelassen: SessionStart-Hook (handoff.md wird per `@` geladen, mehr braucht es nicht), UserPromptSubmit-Hooks (kosten bei jedem Prompt), Hooks, die Tests bei Fehlschlag erzwingen oder im Stop-Hook ausführen.

### 2d `.gitignore`

`__pycache__/`, `*.pyc`, `.pytest_cache/`, `.DS_Store`, `.claude/settings.local.json`. Nicht ignorieren: `.claude/handoff.md`, `.claude/settings.json`.

Prüfen: `python3 -m json.tool .claude/settings.json > /dev/null`; `bash -n .claude/hooks/*.sh`; Simulationen mit Exit-Code-Tabelle im Bericht:
- `echo '{"tool_input":{"file_path":"update.py"}}' | bash .claude/hooks/check.sh; echo exit=$?` (erwartet 0)
- `echo '{"tool_input":{"file_path":"docs/index.html"}}' | bash .claude/hooks/check.sh; echo exit=$?` (erwartet 0; falls der ID-Test an der unveränderten Datei scheitert, den Test anpassen, nicht die Datei)
- `echo '{"tool_input":{"command":"git push origin main"}}' | bash .claude/hooks/guard.sh; echo exit=$?` (erwartet 2)
- `echo '{"tool_input":{"command":"git push origin claude/x && git log --oneline main -3"}}' | bash .claude/hooks/guard.sh; echo exit=$?` (erwartet 0)
- `echo '{"tool_input":{"command":"python3 -m py_compile update.py"}}' | bash .claude/hooks/guard.sh; echo exit=$?` (erwartet 0, keine Ausgabe)
- `echo '{"tool_input":{"command":"grep -n \"import update\" tests/test_update.py"}}' | bash .claude/hooks/guard.sh; echo exit=$?` (erwartet 0, keine Ausgabe)
- `echo '{"tool_input":{"command":"python3 update.py"}}' | bash .claude/hooks/guard.sh; echo exit=$?` (erwartet 0 und die JSON-Zeile mit `"permissionDecision":"ask"`)
- `echo '{}' | bash .claude/hooks/stop.sh; echo exit=$?` (erwartet 0; die JSON-Zeile nur, wenn `git status --short` etwas zeigt)
- `python3 tools/check_data.py`, `python3 tools/check_html.py`, `python3 tools/stats.py` laufen grün und zeigen plausible Zahlen (TikTok-Follower über 2800).
Dann eine Datei minimal editieren, prüfen, dass der Hook automatisch läuft, Änderung zurücknehmen. Falls die Session im manuellen Modus läuft: notiere im Bericht, ob `python3 tools/check_data.py` und `bash .claude/hooks/check.sh` ohne Rückfrage liefen (das ist der Praxistest der Allowlist).

---

## Phase 3: Projekt-Skills in `.claude/skills/<name>/SKILL.md`

Format: Ordner pro Skill, `SKILL.md` mit YAML-Frontmatter (`name`, `description`, optional `disable-model-invocation`, `allowed-tools`, `model`) und Markdown-Body. Aufruf mit `/name`; Claude lädt Skills ohne `disable-model-invocation` auch selbst, wenn die `description` zur Aufgabe passt. Einen automatischen Trigger zum Sessionstart gibt es für Skills nicht; `/briefing` rufe ich selbst auf. Budget: `description` maximal 2 Sätze (wird in jeder Session geladen), Body maximal 60 Zeilen. Skills mit Nebenwirkungen bekommen `disable-model-invocation: true`, damit Claude sie nur auf meinen Befehl lädt. Kein Skill-Name darf mit einem eingebauten Befehl, einem Alias oder meinen Konto-Skills kollidieren (`/review` ist der Alias von `/code-review`, deshalb heißt der Prüf-Skill `diff-check`; `spacefacts-*` und `konkurrenz-video-forensik` sind vergeben). Frontmatter-Listen wie `allowed-tools` dürfen laut Doku als kommagetrennter String stehen.

Das sind zugleich meine "Token-Spar-Skills" und "GitHub-Skills". Lege genau diese 9 an:

| Skill | Zweck | Trigger | Nur manuell |
|---|---|---|---|
| `briefing` | Lädt für eine Aufgabe nur das Nötige: `.claude/handoff.md` ist schon im Kontext, dazu `git log --oneline -5`, `git status`, dann nur die Datei(en) zur Aufgabe. Suche über mehrere Dateien an den eingebauten Explore-Subagenten. Gibt einen 10-Zeilen-Lagebericht. | `/briefing` (rufe ich zu Beginn jeder Session auf), "leg los mit ...", "was ist der Stand" | nein |
| `handoff` | Schreibt `.claude/handoff.md` neu (ersetzen, nicht anhängen, max. 40 Zeilen): Erledigt / Offen / Nächster Schritt / geprüfte Befehle / Branch und PRs; committet sie und nennt zum Schluss Branch-Name und PR-Link im Chat. Danach Empfehlung: CLI `/clear`, Web neue Session aus der Seitenleiste auf demselben Branch; oder `/compact` mit Fokus. | "Pause", "Übergabe", "Session zu Ende", Kontext wird eng | ja |
| `kompakt` | Fasst in 5 Zeilen zusammen, was behalten werden muss (Branch, geänderte Dateien, offene Entscheidung), und gibt mir den fertigen Fokus-Text für `/compact <fokus>`. Ändert nichts. | "Kontext voll", "kompakt", vor langen Aufgaben | ja |
| `pr` | Falls nicht schon auf einem `claude/`-Branch: `git fetch origin main && git switch -c claude/<thema> origin/main`. Checks (py_compile, unittest, check_data, check_html), `git diff --stat main` auf versehentliche Änderungen an `docs/data.json`, `HANDLES`, `update.yml`, Commit auf Deutsch (`Fix: ...` / `Setup: ...`), Push auf den Branch, PR mit Vorlage aus `.github/pull_request_template.md` (Web: GitHub-MCP `create_pull_request`, CLI: `gh pr create`). Nie auf main, nie mergen. | "PR erstellen", "committen", "fertig machen" | ja |
| `diff-check` | Liest den Diff (`git diff main...HEAD` oder PR-Nummer), prüft gegen die Invarianten in CLAUDE.md, listet maximal 7 Befunde nach Schwere mit Datei:Zeile und Vorschlag. Diffs über 200 Zeilen an den Agent `pruefer` delegieren. Ändert nichts. Für den generischen Bug-Blick zusätzlich das eingebaute `/code-review`. | "schau drüber", "prüf den Diff", vor jedem Merge | nein |
| `scraper-fix` | Reparatur eines Abrufs ohne Live-Trial-and-Error mit Fixtures (vollständiges Beispiel unten). | data.json zeigt null oder unplausible Werte, "TikTok-Zahlen fehlen" | nein |
| `dashboard-preview` | `cd docs && python3 -m http.server 8000` im Hintergrund, `tools/check_html.py`, Handy-Viewport 390px bedenken. Browser-Prüfung nur, falls in der Session ein Browser-Tool existiert; sonst reicht `check_html.py`. Änderungen an `index.html` nur mit dieser Prüfung. | jede Änderung an docs/index.html, "sieht das gut aus" | nein |
| `wochenbericht` | `python3 tools/stats.py --days 30` ausführen (nie data.json lesen) und einen deutschen Bericht schreiben: Stand, Deltas, Tempo, Prognosedatum 10k, beste und schwächste Tage, Datenlücken, 3 konkrete Content-Hinweise. Keine Zahl erfinden. Auf Wunsch als `reports/YYYY-WW.md` (Hinweis: das Repo ist öffentlich). | "Wochenbericht", "wie läuft die Mission", montags | nein |
| `data-repair` | Einen Eintrag in `docs/data.json` per Python-Skript (nie per Editor) korrigieren, nur vorhandene Schlüssel (`tiktok.f/l`, `youtube.f/v`, `instagram.f`); Instagram-Follower aus einem Issue "Zahlen nachtragen" als `instagram.f` eintragen. TikTok-Views gehören erst in data.json, wenn `series()` in `index.html` `e.tiktok.v` aus data.json liest (heute wird `v` dort fest auf null gesetzt); bis dahin im Bericht als "noch nicht speicherbar" vermerken. Dann `tools/check_data.py`, Commit `Fix: Daten <datum> korrigiert`, schnell per PR mergen lassen, bevor der Bot wieder schreibt; bei Konflikt Rebase auf main. | falscher Wert, Ausreißer, Issue mit Label `zahlen` | ja |

Vollständiges Beispiel `.claude/skills/scraper-fix/SKILL.md` (die anderen im selben Stil):

```markdown
---
name: scraper-fix
description: Repariert einen ausgefallenen Abruf in update.py (TikTok, YouTube, Instagram) anhand gespeicherter HTML-Fixtures statt Live-Versuchen. Nutzen, wenn data.json null oder unplausible Werte zeigt.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Scraper reparieren

## Ablauf
1. Symptom festhalten: `python3 tools/stats.py --days 7`.
2. Fixture holen, genau einmal: `python3 -c "import urllib.request;r=urllib.request.Request('https://www.tiktok.com/@spacefactswow',headers={'User-Agent':'Mozilla/5.0'});open('tests/fixtures/tiktok_$(date +%F).html','wb').write(urllib.request.urlopen(r,timeout=25).read())"` (Plattform und URL anpassen; fragt nach Erlaubnis). Cookies oder Tokens im Fixture schwärzen, Datei auf die relevanten Ausschnitte kürzen (unter 50 KB).
3. Zielzahl im Fixture lokalisieren: `grep -o '"followerCount":[0-9]*' tests/fixtures/...` bzw. `grep -n -i 'Follower' ...`. Nie die ganze Datei mit Read öffnen.
4. In `update.py` den Parser anpassen. Reihenfolge: JSON-Block parsen (z. B. `__UNIVERSAL_DATA_FOR_REHYDRATION__`) vor Regex; alte Regex als Fallback behalten. `merge()` und die Schlüssel `f/l/v` nicht ändern.
5. Test in `tests/test_update.py` ergänzen, der das Fixture liest und den erwarteten Wert prüft. `python3 -m unittest discover -s tests -v` muss grün sein.
6. Erst jetzt ein einziger Live-Lauf: `python3 update.py` (fragt nach Erlaubnis). Ausgabe prüfen, dann `git checkout docs/data.json`.
7. Commit `Fix: <Plattform>-Abruf repariert (<was>)`, dann `/pr`.

## Regeln
- Keine neuen Abhängigkeiten, nur `urllib`, `re`, `json`.
- Keine Schleifen gegen die Live-Seite; jede Iteration läuft gegen das Fixture.
- Wenn eine Plattform Login verlangt (Instagram): nicht umgehen, sondern im Bericht als "manuell" vorschlagen.
```

Bewusst nicht installiert: Drittanbieter-Token-Skills (`rescue-tokens` aus valorisa/Claude-Skills, `context-mode`-MCP). Für ein 5-Dateien-Repo sparen sie nichts, ein MCP-Server kostet selbst Kontext, und der Pflegestatus ist unklar. `briefing`, `handoff`, `kompakt`, die `Read`-Sperre für data.json, `tools/stats.py` und der Subagent decken das ab.

Prüfen: `ls .claude/skills/*/SKILL.md` zeigt 9 Dateien; jedes Frontmatter hat `name` (gleich dem Ordnernamen) und `description`. Bericht: Liste der Skills mit Zeilenzahl der Beschreibung; Hinweis für mich, ob Projekt-Skills auf dem Web sofort erscheinen oder eine neue Session brauchen (bitte prüfen).

---

## Phase 4: Subagent (genau einer)

Die eingebauten Subagenten `Explore` (schnell, nur lesen) und `Plan` reichen für Suche und Planung. Lege zusätzlich `.claude/agents/pruefer.md` an, damit lange Diffs und Workflow-Logs nicht im Hauptkontext landen:

```markdown
---
name: pruefer
description: Nur-Lese-Prüfer für lange Diffs, Workflow-Logs und Fixtures. Liefert maximal 20 Zeilen mit Datei:Zeile und Vorschlag zurück.
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 15
---
Du prüfst, du änderst nichts. Bash nur für `git diff`, `git log`, `git show` und `python3 tools/...`; nie Edit, Write, `python3 update.py` oder Push. Vergleiche gegen CLAUDE.md (Schema, merge(), stdlib only, Deutsch). Antworte als Liste nach Schwere, maximal 20 Zeilen.
```

Bash bleibt drin, weil der Agent den Diff selbst ziehen soll; die Permission-Regeln aus `settings.json` und `guard.sh` gelten auch für ihn. Prüfen: Frontmatter valide. Bericht: eine Zeile. Aufruf für mich: `@"pruefer (agent)" ...` oder automatisch über `/diff-check`.

---

## Phase 5: Plugins und Marketplaces

`/plugin` gibt es nur in der CLI, nicht in Web-Sessions. Für das Web deklarierst du Plugins unter `enabledPlugins` in `.claude/settings.json`; dokumentierte Form: `"enabledPlugins": {"commit-commands@claude-plugins-official": true}`. Die CLI-Befehle kommen als Block "Lokal einmalig ausführen" in `.claude/CHEATSHEET.md` (Phase 7). Wenn `/plugin` bei dir funktioniert, führe es aus und melde `/plugin list` vorher und nachher.

Empfohlen (offizieller Marketplace `claude-plugins-official`, automatisch registriert):
1. `/plugin install github@claude-plugins-official` (GitHub-MCP für die CLI). In meinen Web-Sessions ist der GitHub-MCP-Server bereits verbunden: dort nicht in `enabledPlugins` eintragen, doppelte Tool-Listen kosten Kontext (bitte prüfen: `/mcp` in der Web-Session zeigt `github`).
2. `/plugin install commit-commands@claude-plugins-official` (optional; der `pr`-Skill deckt das Nötigste ab). Fürs Web in `enabledPlugins` eintragen.
3. Danach `/reload-plugins`. Die eingebauten `/code-review` und `/security-review` reichen als Review-Werkzeuge; kein separates Review-Plugin.
4. `security-guidance` (offiziell wie im Katalog) ist NICHT vorinstalliert und wird bewusst nicht installiert: es hängt Hooks an SessionStart, UserPromptSubmit, PostToolUse und Stop und startet nach jedem Zug mit Dateiänderungen und bei jedem Commit einen zusätzlichen Opus-Review-Aufruf, der auf mein Kontingent zählt. Das Repo hat keine Secrets und keine Nutzereingaben; `/security-review` vor jedem PR reicht. Opt-in-Befehl kommt ins Cheat Sheet.

Aus meinem claude.ai-Katalog (Marketplace `knowledge-work-plugins`): Das GitHub-Repo `anthropics/knowledge-work-plugins` existiert (Apache-2.0) und enthält 11 Plugins (`productivity`, `sales`, `customer-support`, `product-management`, `marketing`, `legal`, `finance`, `data`, `enterprise-search`, `bio-research`, `cowork-plugin-management`). Für die CLI: `/plugin marketplace add anthropics/knowledge-work-plugins`, danach zum Beispiel `/plugin install marketing@knowledge-work-plugins`. `engineering`, `design`, `security-guidance` und die Anbieter-Plugins gibt es nur im claude.ai-Katalog; die schalte ich selbst in der claude.ai-Oberfläche ein. Empfiehl im Bericht:
- Später sinnvoll: `engineering` (Skills `testing-strategy`, `documentation`, `tech-debt`), `data` (`explore-data`, `create-viz`, `validate-data`) für die Auswertung von `data.json`, `marketing` (`performance-report`, `content-creation`) für die Creator-Arbeit. Ich aktiviere sie selbst in der claude.ai-Oberfläche, wenn ich sie brauche.
- Nein, mit Grund: `brightdata-plugin` (bezahlter Scraping-Dienst; das Projekt bleibt kostenlos), `security-guidance` (siehe Punkt 4), `postiz`, `canva`, `adobe-for-creativity`, `miro`, `airtable`, `small-business`, `operations`, `design`, `productivity` (kein Bezug oder Überschneidung mit den Projekt-Skills), LSP-Plugins (brauchen lokale Binaries, überdimensioniert).
- MCP-Server ohne Projektbezug (Reise-Connectoren, Notion, Gmail) in Sessions zu diesem Repo per `/mcp` abschalten; Gmail nur bei Bedarf für den Wochenbericht.

Bericht: installiert / in `enabledPlugins` eingetragen / übersprungen mit Grund / ins Cheat Sheet verschoben.

---

## Phase 6: Tests und GitHub-Seite

6a. Tests, damit Hooks und CI etwas zu prüfen haben: `tests/__init__.py` (leer), `tests/fixtures/.gitkeep`, `tests/test_update.py` mit `unittest`, am Anfang `sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))`, dann `import update`. Fälle: `compact('1.2K') == 1200`, `compact('3,456') == 3456`, `compact('2.1M') == 2100000`, `compact('abc') is None`, `merge({'f':10,'l':5},{'f':None,'l':7}) == {'f':10,'l':7}`, `merge(None,{'f':1}) == {'f':1}`, `grab([r'"followerCount":(\d+)'], '{"followerCount":42}') == 42`. Kein Netzzugriff, kein Umbau von `update.py`. Prüfen: `python3 -m unittest discover -s tests -v` grün.

6b. `.github/workflows/ci.yml` (kein `paths`-Filter, damit ein Pflicht-Check nie ausbleibt):

```yaml
name: CI
on:
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  check:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m py_compile update.py
      - run: python -m unittest discover -s tests -v
      - run: python tools/check_data.py
      - run: python tools/check_html.py
```

6c. `.github/workflows/watchdog.yml`, der kostenlose Ausfall-Alarm (kein Claude, kein Kontingent): `schedule` mit Cron `0 7 * * *` UTC (der Bot läuft 04:30 UTC plus Verspätung) und `workflow_dispatch`; `permissions: contents: read, issues: write`; `timeout-minutes: 5`; Steps: `actions/checkout@v4`, dann ein Step mit `GH_TOKEN: ${{ github.token }}`, der die Labels anlegt (`gh label create bot-alarm --force` und `gh label create zahlen --force`; GitHub setzt Template-Labels nur, wenn sie existieren), dann `python3 tools/check_data.py --today`; ein Step `if: failure()` mit `GH_TOKEN`, der per `gh issue list --label bot-alarm --state open` prüft, ob schon ein offenes Alarm-Issue existiert, und sonst `gh issue create --title "Abruf fehlgeschlagen $(date -u +%F)" --label bot-alarm --body "..."` mit dem Hinweis auf `/scraper-fix` anlegt. Roter Lauf plus Issue: GitHub schickt mir Mail und Push-Benachrichtigung aufs Handy. `update.yml` bleibt unberührt.

6d. `.github/pull_request_template.md` (Deutsch, kurz): Was / Warum / Wie geprüft (Checkboxen: py_compile, unittest, check_data, check_html, Dashboard-Preview falls index.html) / `docs/data.json` und `update.yml` unverändert (ja/nein).

6e. `.github/dependabot.yml`: `package-ecosystem: github-actions`, `directory: /`, `schedule.interval: weekly`. Hält `checkout@v4` und `setup-python@v5` aktuell.

6f. `.github/ISSUE_TEMPLATE/zahlen.yml`: GitHub-eigenes Issue-Formular (kein Claude-Feature) "Zahlen nachtragen" mit Feldern Datum, TikTok-Gesamtviews, Instagram-Follower, Label `zahlen` (Label legt der Watchdog an; bis zu seinem ersten Lauf im Bericht als manueller Schritt: GitHub Issues > Labels > New label `zahlen`, oder `gh label create zahlen`). Damit kann ich vom Handy aus Werte melden, die heute nur im localStorage liegen; `/data-repair` trägt Instagram ein, TikTok-Views erst, wenn `index.html` `e.tiktok.v` aus data.json liest. Keine Auto-Verarbeitung in dieser Session.

6g. Claude GitHub App für `@claude`-Reviews: nicht selbst ausführen, keine `claude.yml` committen (ohne App und Secret wäre jeder PR-Check rot). In den Bericht: `/install-github-app` in der CLI im Repo starten; es installiert die App, legt das Secret (`ANTHROPIC_API_KEY` oder `CLAUDE_CODE_OAUTH_TOKEN`) an und bereitet einen PR mit `.github/workflows/claude.yml` (`anthropics/claude-code-action@v1`) vor. Nur der interaktive Modus (`@claude`-Erwähnung), kein Automations-Job auf jedem PR. Hinweis: mit `ANTHROPIC_API_KEY` kostet jeder Aufruf Guthaben, mit `CLAUDE_CODE_OAUTH_TOKEN` (erzeugt mit `claude setup-token`, geht auf Pro und Max) läuft er über mein Abo-Kontingent. Für `/install-github-app` muss `gh` installiert und angemeldet sein. Optional; `/diff-check` und `/code-review` in der Session reichen meist.

6h. Branch-Schutz für `main` (nur ich, GitHub-Web: Settings > Branches): Achtung, der Bot pusht direkt auf `main`. Beschreibe zwei Varianten: (A) nur "Block force pushes", einfach und bot-sicher; (B) PR-Pflicht plus Status-Check `check` aus `ci.yml` mit Bypass für GitHub Actions (bitte prüfen: Bypass-Option in Rulesets), vorher mit `workflow_dispatch` testen. Empfehlung A.

Prüfen: neue YAML-Dateien mit `python3 -c "import yaml,sys;[yaml.safe_load(open(f)) for f in sys.argv[1:]]" .github/workflows/ci.yml .github/workflows/watchdog.yml .github/dependabot.yml .github/ISSUE_TEMPLATE/zahlen.yml` (fragt einmal nach; falls PyYAML fehlt, Sichtprüfung und Hinweis); `git diff main --stat` zeigt keine Änderung an `update.yml`, `update.py`, `docs/data.json`. Bericht: Dateiliste, welche Schritte manuell bleiben.

---

## Phase 7: Kontext-Hygiene und Cheat Sheet

In `CLAUDE.md`, Abschnitt `## Kontext-Hygiene` (max. 10 Zeilen, für Claude):
- `docs/data.json` nie lesen (Read ist gesperrt); Zahlen nur über `python3 tools/stats.py`.
- Suche über mehrere Dateien an den Explore-Subagenten, lange Diffs und Logs an `pruefer`; nur Ergebnisse in den Hauptkontext.
- Dateien einmal lesen, danach gezielt mit Grep. Große Ausgaben kürzen: `| tail -20`, `--stat`, `-q`.
- Bei Änderungen an mehr als 2 Dateien oder am Schema zuerst Plan-Modus, dann umsetzen.
- Nach abgeschlossenen Aufgaben `/handoff` vorschlagen. Antworten kurz, keine ungefragten Code-Erklärungen.

`.claude/CHEATSHEET.md` (max. 60 Zeilen, wird nicht automatisch geladen, ist für mich):
- Modell je Aufgabe: `sonnet` Alltag, `/model opus` oder `opusplan` (Opus plant, Sonnet setzt um) für Umbauten, `haiku` für reine Nachfragen, `best` nur für die schwersten Aufgaben. Standardmodell ist auf Pro `sonnet`, auf Max `opus`. Modellwechsel mitten in der Session vermeiden (Cache geht verloren). Effort: Standard ist `high`; `/effort medium` für Routine, `xhigh` nur für harte Fehler. Auf dem Web `/model` und `/effort` mit Argument aufrufen.
- Sessions: eine Aufgabe pro Session. Start `/briefing`, Ende `/handoff`. Danach CLI: `/clear`; Web: neue Session aus der Seitenleiste, auf demselben `claude/`-Branch, solange der PR nicht gemergt ist. Bei langem Verlauf `/kompakt`, dann `/compact <fokus>`. Vorher `/context` anschauen (beides geht auch auf dem Web). Fortsetzen: CLI `claude --continue` oder `/resume`; Web: alte Session in der Seitenleiste öffnen (dort gibt es kein `/resume` und kein `/clear`).
- Bei Usage-Limit: erst `/compact`, dann `haiku`, dann Pause. `/fast` nie (teuer, hier ohne Nutzen). `/usage` wöchentlich, `/doctor` nach Setup-Änderungen, `/insights` monatlich (nur CLI).
- Modus: Shift+Tab (CLI) bzw. Modus-Wähler (Web) zwischen Auto, `acceptEdits` und Plan. `/permissions` zeigt die Regeln; `/fewer-permission-prompts` (eingebauter Skill) nach ein paar Sessions, um die Allowlist aus echten Transkripten zu erweitern.
- `/mcp`: für dieses Repo nur GitHub verbunden lassen.
- Opt-in, bewusst nicht aktiv: `/plugin install security-guidance@claude-plugins-official` (kostet pro Zug einen Review-Aufruf).
- Block "Lokal einmalig ausführen" (nur CLI): Plugin-Befehle aus Phase 5, `/install-github-app`, `/web-setup`, lokale Settings aus Phase 8.

Prüfen: Zeilenbudgets eingehalten; das Cheat Sheet enthält keine Befehle, die nicht in diesem Auftrag stehen. Bericht: 2 Zeilen.

---

## Phase 8: Optionale lokale Schritte (nur Anleitung, nicht ausführen)

Für die CLI auf meinem Rechner, gehört nicht ins Repo. Schreibe in Bericht und Cheat Sheet:
- `~/.claude/settings.json` mit `"model": "sonnet"` (hier statt in der committeten Datei, damit die Modellwahl beim Anlegen einer Web-Session unberührt bleibt), `"autoMemoryEnabled": true` und derselben git/python-Allowlist, falls ich das repo-übergreifend will. Auf dem Web wähle ich das Modell beim Anlegen der Session oder per `/model sonnet`.
- `~/.claude/CLAUDE.md` mit 5 Zeilen: Sprache Deutsch, Antworten kurz, keine Erklärungen ungefragt, immer Branch statt main.
- Statuszeile mit Modell, Kontext-Prozent und Kosten: in der CLI `/statusline` ausführen und in einem Satz beschreiben, was angezeigt werden soll. Claude Code legt das Skript unter `~/.claude/` an und trägt `"statusLine": {"type": "command", "command": "~/.claude/statusline.sh"}` in `~/.claude/settings.json` ein; das Skript bekommt `model.display_name`, `context_window.used_percentage` und die Kosten als JSON auf stdin.
- Auf Windows heißt der Interpreter meist `python` statt `python3`: dann in Hooks und Allowlist beide Schreibweisen eintragen (`Bash(python -m py_compile:*)` zusätzlich) und in `check.sh` `python3` durch `${PYTHON:-python3}` ersetzen.
- `/web-setup` in der CLI, wenn Cloud-Sessions GitHub-Zugriff über mein gh-Token brauchen; `/teleport`, um eine Web-Session in die CLI zu holen.
- Die Hooks brauchen lokal nur `python3` und `bash`; `gh` für die `pr`-Skill-Befehle in der CLI installieren.
- `/doctor` einmal laufen lassen.

---

## Phase 9: Routinen auf Claude Code Web (nur Vorschläge)

Routinen laufen in der Cloud ohne Rückfragen und verbrauchen Kontingent. Nichts anlegen; die tägliche Ausfallprüfung macht `watchdog.yml` kostenlos. Lege `.claude/routines.md` mit einem fertigen Vorschlag für `claude.ai/code/routines` bzw. `/schedule` ab:

1. **Wochenbericht** (empfohlen): montags 07:00 Ortszeit im Web-Formular wählen; das Wochen-Preset braucht keinen eigenen Cron und rechnet die Zeit selbst um. Nur falls du doch einen eigenen Cron über `/schedule update` setzt: `0 5 * * 1` bzw. `0 6 * * 1` (bitte prüfen: ob die Cron-Angabe dort in UTC oder Ortszeit gilt). Repo `maubo-prog/mission-control`, Connector nur GitHub, Prompt: "Führe /wochenbericht aus, schreibe `reports/YYYY-WW.md` auf Branch `claude/report-YYYY-WW` und öffne einen PR mit deutscher Zusammenfassung von max. 15 Zeilen. Kein Push auf main." Eine Ausführung pro Woche.
2. Nicht anlegen: einen täglichen Stats-Wächter als Routine (macht 6c gratis) und `/loop` in einer Web-Session zur Dauerüberwachung (Kontext wächst bei jeder Iteration). Routine-Trigger für GitHub-Events gibt es nur für PR und Release, nicht für Issues.

---

## Phase 10: Abschluss

Checkliste, jede Zeile im Bericht mit Befehl und Ergebnis:
1. `python3 -m json.tool .claude/settings.json > /dev/null`, `bash -n .claude/hooks/*.sh`, die acht Hook-Simulationen aus Phase 2.
2. `python3 -m py_compile update.py`, `python3 -m unittest discover -s tests -v`, `python3 tools/check_data.py`, `python3 tools/check_html.py`, `python3 tools/stats.py`.
3. `wc -l CLAUDE.md .claude/handoff.md .claude/CHEATSHEET.md .claude/skills/*/SKILL.md .claude/rules/*.md` innerhalb der Budgets.
4. Alle 9 SKILL.md haben `name` und `description`; der Agent hat `name` und `description`; YAML aller neuen Workflows parsebar.
5. `git diff main --stat` zeigt keine Änderung an `docs/data.json`, `update.py`, `.github/workflows/update.yml`, `README.md` (Ausnahme erlaubt: ein Abschnitt "Für Entwickler / Claude" in der README, max. 15 Zeilen, mit den Befehlen und dem Hinweis, dass data.json vom Bot geschrieben wird).
6. Allowlist-Praxistest: im Bericht festhalten, welche der Befehle `python3 tools/check_data.py`, `bash .claude/hooks/check.sh` und `git push -u origin claude/...` ohne Rückfrage liefen (im Auto-Modus entscheidet der Klassifikator, dann "nicht prüfbar" schreiben; in der CLI zeigt `/permissions` die aktiven Regeln).
7. `handoff.md` nach dem Muster des Skills `handoff` füllen (der Skill selbst ist nur für mich aufrufbar): Erledigt, Offen, Nächster Schritt, geprüfte Befehle, Branch und PR.

Dann Commits auf dem Branch in sinnvollen Blöcken (`Setup: CLAUDE.md, Rules und Handoff`, `Setup: Settings, Hooks und Tools`, `Setup: Skills und Agent`, `Setup: Tests, CI, Watchdog und Vorlagen`, `Setup: Cheat Sheet und Routinen`), Push auf den Branch und PR gegen `main` mit dem PR-Template, so wie es der Skill `pr` beschreibt. Kein Merge.

Abschlussbericht in genau diesem Format:

```
## Angelegt
- Datei: Zweck, Zeilen, geprüft mit ...
## Übersprungen (mit Grund)
- ...
## Manuell zu erledigen (nummeriert, mit exakten Befehlen oder Klickpfaden, nach Aufwand sortiert)
1. ...
## Offene Fragen (max. 5) und alle "(bitte prüfen: ...)"-Stellen
- ...
## Nächster sinnvoller Schritt
- ein Satz
## PR
- Link
```

Wenn irgendwo etwas nicht funktioniert, schreibe es in "Übersprungen" oder "Offene Fragen", statt es zu umgehen. Beginne jetzt mit Phase 0.

---

# Teil B: Setup-Auftrag für den Produktionsordner (optional, eigene Session)

## So benutzt du Teil B

Erst Teil A abschließen. Dann eine Session starten, deren Arbeitsverzeichnis der Ordner `C:\Users\mauri\OneDrive\Tiktok` ist: entweder die Claude Code CLI auf deinem Windows-Rechner (`claude --model opus` in diesem Ordner) oder die Claude-Desktop-App mit dem Ordner als Arbeitsordner, so wie du sie heute für die Produktion nutzt (dort erscheint der Ordner als `/sessions/<session>/mnt/Tiktok`). Nicht auf dem Web, der Ordner liegt nicht auf GitHub. Kopiere alles ab "Deine Rolle". Die Arbeitsregeln aus Teil A (kleine geprüfte Schritte, Deutsch, Zeilenbudgets, "(bitte prüfen: ...)" statt Behauptungen, Abschlussbericht im selben Format) gelten unverändert. Wichtigste Zusatzregel: In diesem Ordner läuft eine funktionierende Automation; nichts, was sie liest oder schreibt, wird in dieser Session verändert, und keine Regel darf ihr eine Rückfrage aufzwingen.

---

## Deine Rolle und das Ziel

Du bist derselbe Senior-Engineer wie in Teil A und richtest jetzt mein zweites Projekt für Claude Code ein: den Produktionsordner für die Kurzvideos von `@spacefactswow`. Ziel: Renders, Forensik und Cover sollen aus Claude Code heraus laufen, ohne dass Medien oder große JSON-Dateien in den Kontext geraten, und ohne dass die drei vorhandenen Konto-Skills angefasst werden. Motto wie in Teil A: solide und schlank.

## Kontext (Annahmen aus meinen drei Konto-Skills; alles in Phase 0 prüfen)

- Ordner (Windows, OneDrive-synchronisiert, kein Git): `_Doku\tools\` mit `spacemotion.py` (Motion-Graphics-Engine: cairo, PIL, numpy, OpenCV, ffmpeg), `video_forensik.py` (Offline-Messung eigener MP4s), `browser_forensik.js` und `forensik_vergleich.py` (Messung im eingebauten Browser, Vergleichstabelle), `render_v76_82.py` und `_Doku\build_v76_82.py` (Render und Captions), `demo\SpaceMotion_Demo.mp4`; `_Doku\Workflow-Uebersicht.md` (Spielregeln 1 bis 13) und `_Doku\Produktionsstandard_2.0.md` (Regeln mit Datum und Messquelle); `_Doku\Nachbarkanaele.md`; `_Branding\fonts\Montserrat-*.ttf`; `_Stock-Weltraum\*.mp4`; `_Konkurrenz\` mit `_forensik\` und `_forensik\browser\_Vergleich*.md`; `_Trends\Trends_*.md`; `_Reports\KPI-Report_*.md` und `Zahlen-Audit_*.md`; `Content-Index.md` (Videonummern), `Uploadplan.json` (Auto-Upload), `Automation-Log.md`, `tasks\lessons.md`; Videoprojekte als `NN_Thema\` mit `*_Skript.md` (9-Beat-Plan, `[GFX]`-Marker), `*_Plattform-Uploads.md` und `_render\words_LANG.json` (ElevenLabs-Wort-Timings).
- Werkzeuge auf dem Rechner: Python mit den genannten Bibliotheken, ffmpeg und ffprobe. Ob `python` oder `python3`, ob PowerShell oder Git Bash: in Phase 0 feststellen.
- Die vier Konto-Skills (`spacefacts-produktionsauftrag`, `spacefacts-motion-graphics`, `konkurrenz-video-forensik`, `spacefacts-cover-design`) sind auf die Sandbox der Desktop-App geschrieben (120 Sekunden je Bash-Aufruf, `/tmp` wird geleert, Fonts nach `~/.fonts` kopieren, eingebauter Browser für TikTok und ElevenLabs). In der CLI auf meinem Rechner gelten diese Grenzen nicht, die Windows-Pfade darin stimmen dort. Die Skills sind die Wissensbasis und bleiben unverändert; Projekt-Skills dürfen sie ergänzen, nicht kopieren.
- Automation: Es laufen geplante Aufgaben, die täglich in diesen Ordner schreiben (unter anderem ein Nachbarkanal-Task für Video-IDs und ein Seed-Task; beide protokollieren in `Automation-Log.md`), und der Auto-Upload liest `Uploadplan.json`. Diese Dateien, `Content-Index.md`, `tasks\` und die geplanten Aufgaben selbst werden in dieser Session weder geändert noch gelöscht.
- Marke: Gelb #FFEC00 auf Tiefblau #05070F bis #0B1026, Montserrat, Zahlen im Bild als Ziffern in deutscher Schreibung, kein Emoji im Bild. Harte Produktionsregeln: Hook mit Schnitt oder deutlicher Bewegung in den ersten 3 Sekunden, kein Clip zweimal im selben Video, Voiceover auf -15 LUFS, 2 bis 4 Sekunden je Shot, Quellen-Badge im letzten Fünftel.

---

## Phase 0: Bestandsaufnahme (nur lesen)

- Ordnerbaum nur eine Ebene tief je Ordner, mit Größe je Medienordner in einer Zeile (PowerShell: `Get-ChildItem -Directory | ForEach-Object { "{0}`t{1:N0} MB" -f $_.Name, ((Get-ChildItem $_ -Recurse -File | Measure-Object Length -Sum).Sum / 1MB) }`; Git Bash: `du -sh */`). Keine Mediendatei und keine `words_*.json` öffnen.
- `python --version` oder `python3 --version`, `ffmpeg -version`, `ffprobe -version`, `git --version`, `claude --version`. Prüfen, ob `bash` (Git Bash) verfügbar ist; davon hängt die Hook-Form ab.
- `_Doku\Workflow-Uebersicht.md` und `Produktionsstandard_2.0.md` komplett lesen, die Skripte in `_Doku\tools\` und `_Doku\build_v76_82.py` einmal komplett lesen, sonst nichts. `Content-Index.md`, `Uploadplan.json` und `Automation-Log.md` nur mit `tail -20` beziehungsweise `Get-Content -Tail 20` anschauen. Kein Testrender in dieser Phase.
- Geplante Aufgaben, die auf den Ordner zugreifen, nur auflisten (Desktop-App, Bereich Routinen beziehungsweise lokale geplante Aufgaben), nichts ändern.

Bericht: Ordnerbaum (max. 30 Zeilen), Größen, welche Annahmen oben nicht stimmen, welcher Interpreter und welche Shell.

---

## Phase 1: Git nur für Text und Code (Entscheidung von mir)

Frage mich zuerst, bevor du etwas anlegst. Meine Vorgabe: Git nur für Skripte und Markdown, nie für Medien. Empfehlung, die du mir mit Vor- und Nachteilen vorlegst:
- `_Doku` wird ein eigenes privates Repo `spacefacts-studio` (Tools, Skript-Markdown, Produktionsstandard, Trendreports, Forensik-Markdown und -JSON). Vorteil: Claude Code auf dem Web und Routinen können damit arbeiten, jede Regeländerung im Produktionsstandard ist nachvollziehbar, und `mission-control` kann später darauf verweisen.
- `.gitignore`: `*.mp4`, `*.mov`, `*.wav`, `*.mp3`, `*.png`, `*.jpg`, `*.psd`, `_render/`, `__pycache__/`; Ausnahme: Standbilder unter 200 KB, die als Referenz im Produktionsstandard dienen.
- OneDrive und Git vertragen sich schlecht (Dateisperren, Konfliktkopien): entweder das Repo außerhalb von OneDrive halten und `_Doku` dorthin verschieben, oder den Ordner in OneDrive auf "Immer auf diesem Gerät behalten" stellen. Das entscheide ich; bis dahin nur `.gitignore` und `README` vorbereiten, kein `git init`.

---

## Phase 2: `CLAUDE.md` und pfadgebundene Regeln (Budget 80 Zeilen)

`CLAUDE.md` im Ordner, in dem `claude` gestartet wird:
```
# spacefacts Studio                 (1 Zeile: Kurzvideo-Produktion für @spacefactswow, Produktionsstandard 2.0)
## Sprache                          (Deutsch du-Form; Code-Bezeichner Englisch)
## Ordnerkarte                      (je Ordner eine Zeile: Rolle, nicht Inhalt; welche Ordner Medien sind)
## Werkzeuge                        (Renderer-Aufruf aus spacemotion.py, video_forensik.py-CLI, render_v76_82.py; Interpreter- und Shell-Namen aus Phase 0)
## Produktionsregeln                (die harten Regeln aus dem Kontext, je eine Zeile, mit Verweis auf Produktionsstandard_2.0.md als Quelle)
## Marke                            (Farben, Fonts, Ziffern, kein Emoji)
## Kontext-Hygiene                  (Inhalt siehe unten, max. 10 Zeilen)
## Automation                       (welche geplanten Aufgaben täglich laufen und welche Dateien sie besitzen: Automation-Log.md, Uploadplan.json, Content-Index.md, tasks/)
## Nicht anfassen ohne Rückfrage    (_Branding, fertige Videos, Produktionsstandard-Regeln ohne Messwert, die vier Konto-Skills, alles unter Automation)
## Konto-Skills                     (eine Zeile je Skill: wofür; sie sind die Wissensbasis, Projekt-Skills rufen nur Werkzeuge)
```

Kontext-Hygiene (für Claude): Video- und Audiodateien, `words_*.json` und Forensik-JSON nie mit Read öffnen (PNG-Snapshots zur Sichtprüfung sind erlaubt); `Content-Index.md`, `Uploadplan.json` und `Automation-Log.md` nur per Grep oder `tail`; Dauer, Auflösung und Größe über `ffprobe -v error -show_entries format=duration,size:stream=width,height -of csv=p=0 <datei>`; Lautheit über `ffmpeg -i <datei> -af ebur128 -f null - 2>&1 | tail -12`; Forensik nur als `_forensik.md` lesen; Renders in Zeitfenstern (`r.render(out, t0, t1)`) und mit ffmpeg concat zusammensetzen; Frames zur Sichtprüfung als PNG mit `r.snapshot(t, png)` erzeugen und nur diese anschauen; Ausgaben mit `| tail -20` kürzen.

Pfadgebundene Regeln in `.claude/rules/`, je maximal 15 Zeilen:
- `tools.md` (`paths: ["_Doku/tools/**"]`): keine neuen Abhängigkeiten ohne Rückfrage; jede Änderung mit `py_compile` und einem 2-Sekunden-Testrender (`r.render(out, 0, 2)`) prüfen; Zahlenformatierung nur über `fmt_de`.
- `skripte.md` (`paths: ["**/*_Skript.md"]`): 9-Beat-Struktur beibehalten, 3 bis 4 Grafik-Beats markieren (Beat 1 immer Kinetic-Hook), jeder Fakt mit Quelle, Zahlen im Sprechtext ausgeschrieben.
- `standard.md` (`paths: ["_Doku/Produktionsstandard_2.0.md"]`): keine Regel ohne Messwert, Datum und Quelle; bestehende Regeln nur ergänzen, nie stillschweigend ändern.

Prüfen: `wc -l` (oder PowerShell `Measure-Object -Line`) innerhalb der Budgets. Bericht: 3 Zeilen.

---

## Phase 3: `.claude/settings.json` und Hooks

Vorsicht: In diesem Ordner laufen der Produktionsauftrag und geplante Aufgaben ohne manuelle Schritte. Jede `ask`- oder `deny`-Regel, die eine Datei oder einen Befehl trifft, den diese Läufe brauchen, würde sie stoppen. Deshalb nur Regeln, die die Automation nie berührt:
- `allow`: `Bash(python -m py_compile:*)` und die `python3`-Variante, `Bash(python _Doku/tools/*)`, `Bash(python3 _Doku/tools/*)`, `Bash(python _Doku/build_v76_82.py:*)`, `Bash(python3 _Doku/build_v76_82.py:*)`, `Bash(ffmpeg:*)`, `Bash(ffprobe:*)`, `Bash(git status:*)`, `Bash(git diff:*)`, `Bash(git log:*)`, `Bash(ls:*)`, `Bash(du -sh:*)`, `Bash(tail:*)`, `Bash(grep:*)`.
- `deny`: `Read(**/*.mp4)`, `Read(**/*.mov)`, `Read(**/*.wav)`, `Read(**/*.mp3)` (Video und Audio lassen sich mit Read ohnehin nicht sinnvoll lesen; PNG bleibt erlaubt, weil die Frame-Prüfung nach dem Render Snapshots anschaut), `Bash(rm -r*)`, `Bash(Remove-Item * -Recurse*)`, `Bash(rmdir /s*)`.
- Kein `ask` für Render-, Upload- oder Automationsdateien. Der Schutz für `Uploadplan.json`, `Content-Index.md`, `Automation-Log.md` und `tasks\` steht in CLAUDE.md, nicht in den Permissions.
- Hook `PostToolUse` auf `Edit|Write`: nur für `*.py` `py_compile`, für `Produktionsstandard_2.0.md` prüfen, dass jede neue Regelzeile ein Datum enthält (Regex `20\d\d-\d\d-\d\d`), sonst Exit 2 mit Hinweis. Für alle anderen Dateien sofort Exit 0; der Hook darf nie länger als 2 Sekunden laufen, damit die Automation nicht hängt. Hook-Skript als `.ps1`, wenn Phase 0 keine `bash` gefunden hat (bitte prüfen: Hook-Ausführung unter PowerShell auf deiner Version, Doku-Seite hooks, Abschnitt zu PowerShell).
- Kein Stop-Hook, kein `SessionStart`-Hook. (bitte prüfen: ob die Desktop-App `.claude/settings.json` und Hooks aus dem Arbeitsordner liest; falls nicht, wirken die Regeln nur in der CLI.)

Prüfen: JSON valide, Hook mit `echo '{"tool_input":{"file_path":"_Doku/tools/spacemotion.py"}}' | ...` simuliert, Exit-Codes im Bericht.

---

## Phase 4: Projekt-Skills (Ergänzung zu den Konto-Skills, keine Kopie, je max. 40 Zeilen)

Kein `wochenbatch`- und kein `forensik`-Skill: das machen `spacefacts-produktionsauftrag` und `konkurrenz-video-forensik` bereits. Nur diese drei:

| Skill | Zweck | Nur manuell |
|---|---|---|
| `render-check` | Für ein fertiges Video: ffprobe-Zusammenfassung, Lautheit über `ebur128`, Vergleich erster und letzter Frame (Loop-Schnitt) über zwei Snapshots, ohne das Video zu lesen. Ergebnis 10 Zeilen. | nein |
| `briefing` | Wie in Teil A, angepasst: `tail -20 Automation-Log.md`, letzte Zeilen von `Content-Index.md`, `git status` falls Git, dann nur die Dateien zur Aufgabe. | nein |
| `handoff` | Wie in Teil A, schreibt `.claude/handoff.md` in diesem Ordner. `tasks/lessons.md` nicht anfassen, das gehört dem Produktionsauftrag. | ja |

Jeder Skill nennt am Anfang, welcher Konto-Skill die Regeln liefert, und ruft nur Werkzeuge in fester Reihenfolge auf.

---

## Phase 5: Abschluss

Checkliste wie in Teil A: JSON valide, Hook simuliert, `py_compile` auf die Tools, Zeilenbudgets, ein 2-Sekunden-Testrender mit `spacemotion.py` und ein `render-check` auf die Demo-Datei. Abnahmetest für die Automation: Ich starte danach selbst einen Produktionsauftrag mit einem Video; entsteht dabei eine neue Rückfrage oder ein Hook-Fehler, wird die verursachende Regel entfernt, nicht die Automation angepasst. Bericht im Format aus Teil A. Kein `git init` und kein Commit, bevor ich Phase 1 entschieden habe. Beginne jetzt mit Phase 0.

---

# Teil C: Vorschläge über das Setup hinaus

### Projekt-Robustheit (Reihenfolge nach Nutzen pro Aufwand, je ein eigener kleiner PR)

1. **Ausfall sichtbar machen in `update.py` und `update.yml`**: `update.py` weiter mit Exit 0 beenden, aber pro gescheiterter Quelle eine `::warning::`-Zeile ausgeben und bei `tiktok.f` None eine Markierung für den Workflow schreiben. In Python: `p = os.environ.get("GITHUB_OUTPUT"); p and open(p, "a").write("tiktok_null=1\n")` (lokal ohne die Variable passiert nichts). In `update.yml` bekommt der Python-Step `id: run`, und nach dem Commit-Step folgt ein letzter Step `if: steps.run.outputs.tiktok_null == '1'` mit `run: exit 1`.
   - Warum nicht einfach `sys.exit(1)` im Skript: dann würde der Commit-Step übersprungen und der Tageseintrag ginge komplett verloren, schlimmer als das heutige stille null. Mit der Markierung wird data.json committet und der Lauf trotzdem rot; roter Workflow = automatische GitHub-Mail. Das berührt `update.yml`, das im Setup eingefroren ist, also bewusst als eigener PR und danach einmal per `workflow_dispatch` testen. Der `watchdog.yml` aus dem Setup fängt Ausfälle schon ab, aber erst um 07:00 UTC.
2. **TikTok-Parser auf JSON umstellen**: Die Profilseite enthält `<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__">`. `json.loads` darauf und `userInfo.stats.followerCount/heartCount/videoCount` lesen; Regex nur als Fallback.
   - Behebt die seit 12.08. gerundeten Likes und schützt die Follower-Zahl vor demselben Ausfall. Mit `/scraper-fix` und einem Fixture in einer Session machbar.
3. **YouTube-Views über die Data API v3**: `channels?part=statistics&forHandle=spacefactswow&key=...`, kostenlos, 1 Quota-Einheit pro Tag. API-Key als Repository-Secret `YT_API_KEY`, in `update.py` per `os.environ` lesen, Scraping bleibt Fallback.
   - Bis dahin `youtube.v` im Dashboard aus "Gesamt Views" nehmen; die aktuelle Zahl ist Rauschen (16, 970, 71, 75).
4. **Manuelle Werte ins Repo holen**: TikTok-Gesamt-Views und Insta-Follower liegen nur im localStorage eines Handys. Handywechsel oder Browser-Reset = Daten weg, 100k-Balken leer.
   - Bester Weg: `workflow_dispatch`-Inputs in `update.yml` (`tiktok_views`, `instagram_followers`, optional `date`), die `update.py` aus Umgebungsvariablen liest und als `tiktok.v` / `instagram.f` merged. Eingabe dann über github.com im Handy-Browser (Actions > Zahlen aktualisieren > Run workflow); ob die GitHub-App am Handy Inputs anbietet, bitte prüfen. Das Issue-Formular aus dem Setup ist die Übergangslösung.
   - `index.html` muss `e.tiktok.v` zusätzlich zum localStorage lesen (heute wird `v` für jeden Eintrag fest auf null gesetzt); erst danach darf `/data-repair` TikTok-Views in data.json schreiben. `tools/check_data.py` kennt `tiktok.v` bereits als optionalen Schlüssel. Dazu ein "Export/Import als Text"-Knopf im Dashboard als Sicherung.
5. **Instagram ehrlich machen**: Seit Start null, weil Login nötig. Entweder `HANDLES["instagram"] = ""` und im README/Dashboard als "manuell" kennzeichnen, oder Instagram Graph API mit Creator-Konto und Long-Lived-Token als Secret.
   - Bright Data wäre die bezahlte Abkürzung, für ein kostenloses Projekt nicht sinnvoll.
6. **Workflow-Härtung von `update.yml`**: `concurrency: {group: stats-update, cancel-in-progress: false}`, `timeout-minutes: 10`, `git pull --rebase origin main` vor `git push`. Actions bleiben auf Major-Tags (`@v4`, `@v5`), Dependabot aus dem Setup hält sie aktuell; das passt zur Regel in `.claude/rules/workflows.md`.
   - Verhindert Push-Fehler, wenn ein manueller Start mit dem Cron-Lauf kollidiert. Lässt sich mit Vorschlag 1 in einem PR erledigen, danach einmal per `workflow_dispatch` testen.
7. **`fetch()` mit Retry und Logausgabe**: 2 bis 3 Versuche mit 2/5/10 s Pause, HTTP-Status prüfen, pro Quelle eine Zeile "direkt / jina / Textfallback". Das Actions-Log erklärt sich dann selbst.
   - Datum in UTC berechnen (`datetime.datetime.now(datetime.timezone.utc).date()`), damit ein lokaler Lauf nachts keinen zweiten Tageseintrag erzeugt.
8. **Dashboard**: Chart mit `role="img"`, `aria-label`, Min/Max-Beschriftung und Legende; Tabs als `role="tablist"`.
   - Später `manifest.webmanifest` plus minimaler Service Worker (stale-while-revalidate für `data.json`), damit die Home-Screen-App offline die letzten Zahlen zeigt. Alles ohne Build-Step.
9. **README**: Abschnitte "Bekannte Grenzen" (Instagram, YouTube-Views, Cron-Verspätung, Winterzeit 05:30 MEZ) und "Für Entwickler / Claude" mit den Befehlen aus CLAUDE.md; Tabelle der Dateien um `data.json`, `tests/` und `tools/` ergänzen.

### Creator-Workflow (optionale zweite Ausbaustufe)

Das Setup hält den Creator-Teil bewusst klein (`/wochenbericht`). Wenn du mehr willst, in dieser Reihenfolge. Bitte beachten: das Repo ist öffentlich, also gehören Markenstimme, Ideen-Backlog und Posting-Log nach Notion oder in ein privates Repo, nicht nach `mission-control`.

- **Posting-Daten erfassen**: Datum, Plattform, Titel, Views je Video, z. B. als `docs/posts.json` (öffentlich, aber unkritisch) oder als Notion-Datenbank.
  - Erst damit werden Analysen möglich, die über Follower-Kurven hinausgehen (welche Wochentage und Themen laufen). Das ist die wertvollste Datenerweiterung für die 100k-Views-Mission.
- **Skill `content-ideen`**: Ideen-Backlog mit Idee, Hook-Ansatz, Quelle des Weltraum-Fakts (nur belegbare Fakten, Quelle nennen), Status. Pro Aufruf 10 Ideen, priorisiert nach dem, was laut `tools/stats.py` an starken Tagen lief.
- **Skill `hook-caption`**: Für eine Idee drei Hook-Varianten (erste 2 Sekunden), eine Caption, 5 Hashtags je Plattform, in deiner Stimme aus einer privaten `brand.md` (Zielgruppe, Tonalität: staunend, präzise, nie reißerisch, kurze Sätze).
  - Kalibrieren mit 5 Captions, die du gut fandest. Den bereits aktiven `humanizer`-Skill am Ende jeder Caption nutzen.
- **Skill `posting-checkliste`**: Fakt geprüft, Hook in 2 Sekunden, Untertitel, Länge, Cover-Text, Caption, Hashtags, Cross-Posting-Reihenfolge, Eintrag ins Posting-Log.
- **Katalog-Plugins**: `marketing` > `performance-report` als zweite Meinung zum Wochenbericht und `content-creation` für Skripte; `data` > `explore-data` / `create-viz` für Wochentagsmuster und Ausreißer, sobald die Zeitreihe länger ist.
  - `xlsx` hast du aktiv, ein Export von `data.json` nach Excel ist eine Zeile Python. `postiz`, `canva`, `adobe-for-creativity` nur, wenn du wirklich aus Claude heraus planen oder gestalten willst; jeder aktive MCP-Server kostet Kontext.
- **Gmail-Connector**: Wochenbericht montags als Entwurf im Postfach, nur innerhalb der Routine mit Connector-Freigabe; in normalen Sessions per `/mcp` aus.

### Token, Kosten und Plan

- Für dieses Repo reicht `sonnet` als Standard; `opus` nur für Umbauten (Parser auf JSON, manuelle Werte ins Repo). Bei wenigen Sessions pro Woche, einer Aufgabe pro Session (CLI `/clear`, Web neue Session) und der `Read`-Sperre auf `data.json` dürftest du die Pro-Limits selten erreichen; prüfe es nach zwei Wochen mit `/usage`.
- Größte Kontingent-Fresser wären die Claude GitHub App bei jedem PR, tägliche Routinen und das `security-guidance`-Plugin (ein Opus-Review-Aufruf pro Zug mit Dateiänderungen). Alles erst einschalten, wenn dir etwas fehlt. Vorher klären, ob Actions-Läufe über `CLAUDE_CODE_OAUTH_TOKEN` auf dein Kontingent zählen oder ein API-Key mit Guthaben nötig ist.
- Wenn du Limits triffst: `/usage` anschauen, `/effort medium`, Sessions konsequenter trennen, Reise- und Notion-Connectoren im Repo-Kontext abschalten. Hohe Cache-Misses in `/usage` bedeuten meist einen Modellwechsel oder `/compact` mitten im Thema.
- Fast-Modus lohnt nie: das Dashboard aktualisiert sich einmal täglich, Latenz ist egal.
- Wenn du später doch externe Token-Skills probieren willst: `rescue-tokens` aus `valorisa/Claude-Skills` als Projekt-Skill kopieren (kein MCP) und den Effekt per `/context` vorher/nachher messen; `context-mode` als MCP-Server nur, wenn du mehrere große Repos hast.

### Zweites Projekt: Videoproduktion und die drei Konto-Skills

- **Vier Konto-Skills, eine Umgebung**: Die Sandbox der Desktop-App (Ordner unter `/sessions/<session>/mnt/Tiktok`, eingebauter Browser, 120 Sekunden je Bash-Aufruf) ist deine Hauptumgebung für die Produktion. Halte die Sandbox-Regeln in jedem Skill in einem klar benannten Abschnitt am Anfang zusammen und ergänze einen Satz, was in der Claude Code CLI anders ist (kein Zeitlimit, Windows-Pfade, kein eingebauter Browser). Der `skill-creator`-Skill, den du aktiv hast, kann die vier Skills gemeinsam umbauen und die Beschreibungen auf Trigger-Genauigkeit testen. `spacefacts-produktionsauftrag` und `konkurrenz-video-forensik` überschneiden sich bei der Forensik-Abnahme; ein Verweis statt Doppelung spart bei jedem Lauf Kontext.
- **Produktionsstandard versionieren**: `_Doku/Produktionsstandard_2.0.md` ist deine wichtigste Datei und liegt nur in OneDrive. Als privates Repo (Teil B, Phase 1) bekommt jede Regel eine Historie, und Claude Code auf dem Web kann sie lesen, ohne dass du am Rechner sitzt.
- **Dashboard und Produktion verbinden**: `Content-Index.md`, `Uploadplan.json` und die KPI-Reports kennen jedes Video mit Nummer und Datum, `mission-control` kennt nur die Kanalsumme. Ein kleiner Export (`docs/posts.json`: Datum, Plattform, Videonummer, Views nach 24 Stunden und 7 Tagen), den der Produktionsauftrag am Ende schreibt und der per Commit ins Dashboard-Repo gelangt, verknüpft die Forensik-Kennzahlen deiner Videos mit den echten Zahlen. Erst damit lässt sich prüfen, ob die Regeln des Produktionsstandards (Schnitte pro Minute, Hook-Bewegung) wirklich mit Views korrelieren. `/wochenbericht` kann das Log dann mit auswerten.
- **Medien nie in den Kontext**: Die `deny`-Regeln für `Read` auf Medien und `words_*.json` (Teil B) sind der wichtigste Token-Sparer für dieses Projekt. Ein einziges gelesenes Timing-JSON oder Forensik-JSON kann mehr Kontext kosten als das ganze `mission-control`-Repo.
- **Cover-Skill und Dashboard-Optik**: `spacefacts-cover-design` und `docs/index.html` nutzen dieselbe Marke (Gelb #FFEC00, Tiefblau, Montserrat). Ein gemeinsames `brand.md` (Farben, Fonts, Abstände, Beispiel-Cover) in `_Branding` spart in beiden Projekten Erklärungen und gehört als `@`-Import nur in die CLAUDE.md des Produktionsordners.

### Was du selbst entscheiden solltest

1. Branch-Schutz auf `main`: nur Force-Push-Verbot (einfach, bot-sicher) oder PR-Pflicht mit Bypass für den Bot.
2. Claude GitHub App ja/nein, und falls ja: API-Key (Geld) oder OAuth-Token (Abo-Kontingent).
3. YouTube Data API: kostenlosen API-Key in der Google Cloud Console anlegen (10 Minuten) oder weiter ohne Views leben.
4. Instagram: manuell pflegen oder Graph API mit Creator-Konto einrichten.
5. Manuelle Werte: `workflow_dispatch`-Inputs (schneller, eine Änderung an `update.yml`) oder Issue-Formular plus Auto-Verarbeitung (bequemer am Handy). In beiden Fällen muss `index.html` vorher `e.tiktok.v` lesen.
6. Wochenbericht als Routine (Cloud, verbraucht Kontingent) oder auf Zuruf mit `/wochenbericht` in einer Session.
7. Ob du Posting-Daten erfassen willst; erst damit lohnt sich die Creator-Ausbaustufe.
8. Ob `_Doku` aus dem Produktionsordner ein privates Repo wird (Teil B, Phase 1) und wo es liegt (in oder außerhalb von OneDrive).
