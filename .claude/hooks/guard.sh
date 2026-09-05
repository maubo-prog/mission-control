#!/usr/bin/env bash
# PreToolUse vor Bash: sperrt Push nach main und Force-Push, erzwingt Rueckfrage vor dem Live-Scraper.
# Exit 2 = Befehl blockieren, stderr ist die Begruendung. Exit 0 = erlauben, dann wirkt nur JSON auf stdout.
cmd=$(python3 -c 'import json,sys;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
ask=0
# Verkettete Befehle (&&, ||, ;) einzeln pruefen und nur am Segmentanfang matchen, damit
# "git push origin claude/x && git log main" und "grep 'import update' tests/..." nicht anschlagen.
while IFS= read -r part; do
  part="${part#"${part%%[![:space:]]*}"}"
  case "$part" in
    "git push"*" main"|"git push"*" main "*|"git push"*":main"*|"git push"*"--force"*|"git push -f"*)
      echo "Gesperrt: Push nach main oder Force-Push. Nutze einen claude/-Branch und einen PR." >&2
      exit 2 ;;
    "python3 update.py"*|"python update.py"*|"python3 -c "*"import update"*|"python -c "*"import update"*)
      ask=1 ;;
  esac
done < <(printf '%s\n' "$cmd" | tr ';&|' '\n')
if [ "$ask" = 1 ]; then
  printf '%s' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"update.py macht echte Netzabrufe und ueberschreibt den heutigen Eintrag in docs/data.json. Danach git checkout docs/data.json."}}'
fi
exit 0
