#!/usr/bin/env python3
"""Prueft docs/index.html ohne Node und ohne Abhaengigkeiten.

Geprueft wird: html.parser laeuft durch, script-Tags sind balanciert, lang="de" ist
gesetzt, und jede per getElementById("x") geholte ID kommt auch als id="x" im Markup
vor (auch in den Strings, aus denen render() das Markup baut).
Exit 0 = alles in Ordnung, Exit 1 = Fehler.
"""
import pathlib
import re
import sys
from html.parser import HTMLParser

PAGE = pathlib.Path(__file__).resolve().parents[1] / "docs" / "index.html"


class Silent(HTMLParser):
    """Faellt nur auf, wenn html.parser selbst eine Ausnahme wirft."""

    def error(self, message):  # pragma: no cover, nur fuer alte Python-Versionen
        raise ValueError(message)


def main():
    try:
        html = PAGE.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("FEHLER: %s nicht gefunden" % PAGE, file=sys.stderr)
        return 1

    errors = []

    try:
        Silent(convert_charrefs=True).feed(html)
    except Exception as exc:
        errors.append("html.parser bricht ab: %s" % exc)

    opened = len(re.findall(r"<script\b", html, re.I))
    closed = len(re.findall(r"</script\s*>", html, re.I))
    if opened != closed:
        errors.append("script-Tags nicht balanciert: %d geoeffnet, %d geschlossen"
                      % (opened, closed))

    if not re.search(r'<html[^>]*\blang\s*=\s*"de"', html, re.I):
        errors.append('lang="de" fehlt im html-Tag')

    ids = set(re.findall(r'id="([\w-]+)"', html)) | set(re.findall(r"id='([\w-]+)'", html))
    used = set(re.findall(r'getElementById\("(\w+)"\)', html))
    missing = sorted(used - ids)
    for m in missing:
        errors.append('getElementById("%s") hat kein passendes id="%s" im Markup' % (m, m))

    if errors:
        for e in errors:
            print("FEHLER: " + e, file=sys.stderr)
        print("check_html: %d Fehler" % len(errors))
        return 1
    print("check_html: OK, %d IDs referenziert, %d IDs im Markup" % (len(used), len(ids)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
