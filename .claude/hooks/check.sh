#!/usr/bin/env bash
# PostToolUse nach Edit und Write: prueft nur die gerade geaenderte Datei, unter 2 Sekunden.
# Exit 2 blockiert nichts mehr, zeigt Claude aber die stderr-Meldung.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
f=$(python3 -c 'import json,sys;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
[ -n "$f" ] || exit 0
case "$f" in
  *.py)                      python3 -m py_compile "$f" || exit 2 ;;
  *docs/data.json)           python3 tools/check_data.py || exit 2 ;;
  *docs/index.html)          python3 tools/check_html.py || exit 2 ;;
  *.github/workflows/*.yml)  if python3 -c "import yaml" 2>/dev/null; then
                               python3 -c "import yaml,sys;yaml.safe_load(open(sys.argv[1]))" "$f" || exit 2
                             else
                               echo "Hinweis: PyYAML fehlt, YAML nicht geprueft" >&2
                             fi ;;
  *.json)                    python3 -m json.tool "$f" > /dev/null || exit 2 ;;
esac
exit 0
