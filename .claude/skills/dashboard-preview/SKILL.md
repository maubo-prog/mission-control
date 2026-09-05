---
name: dashboard-preview
description: Prueft docs/index.html vor dem Commit, mit lokalem Server und Strukturpruefung, mit Blick auf den Handy-Viewport. Nutzen bei jeder Aenderung am Dashboard und bei "sieht das gut aus".
allowed-tools: Read, Grep, Bash
---
# Dashboard pruefen

## Ablauf

1. Strukturpruefung zuerst, sie ist schnell und faengt das meiste:
   `python3 tools/check_html.py`
   Sie prueft, ob `html.parser` durchlaeuft, die script-Tags balanciert sind, `lang="de"` steht
   und jede per `getElementById` geholte ID im Markup vorkommt.
2. Lokalen Server starten, im Hintergrund:
   `cd docs && python3 -m http.server 8000`
   Danach ist das Dashboard unter `http://localhost:8000/` erreichbar. Der Server laedt
   `data.json` aus demselben Ordner, es braucht keinen Bot-Lauf.
3. Nur wenn diese Session ein Browser-Werkzeug hat: Seite oeffnen, Breite auf 390px stellen,
   pruefen ob etwas horizontal scrollt oder umbricht. Ohne Browser-Werkzeug reicht Schritt 1,
   das dann im Bericht so schreiben statt eine Sichtpruefung zu behaupten.
4. Server danach beenden.

## Worauf zu achten ist

- Zielgeraet ist ein Handy, Viewport 390px. `.wrap` ist auf 440px begrenzt.
- Die Handler `setMetric`, `toggleAll` und `saveManual` werden aus dem `innerHTML` heraus
  aufgerufen und muessen global bleiben.
- Manuelle Werte liegen im localStorage. Eine leere localStorage darf die Seite nicht brechen.
- Faellt `data.json` weg, muss die Fehlermeldung im roten Kasten erscheinen, nicht eine leere Seite.

Erst wenn das gruen ist, committen.
