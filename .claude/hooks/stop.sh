#!/usr/bin/env bash
# Stop: erinnert an uncommittete Aenderungen. Immer Exit 0, sonst kann die Session nicht enden.
# Kein Testlauf hier: reines stdout sieht niemand, und ein Ergebnis, das Claude zu sehen
# bekaeme, wuerde nach dem Stop neue Zuege ausloesen. Tests laufen ueber check.sh, /pr und die CI.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
if [ -n "$(git status --short 2>/dev/null)" ]; then
  printf '%s' '{"systemMessage":"Hinweis: uncommittete Aenderungen vorhanden. Nur zur Info, nichts weiter tun."}'
fi
exit 0
