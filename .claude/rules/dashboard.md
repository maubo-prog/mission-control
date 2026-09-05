---
paths: ["docs/index.html"]
---

# Regeln fuer das Dashboard

- Eine Datei, Vanilla JS, kein Build, keine Module, kein `type="module"`, keine externen Skripte.
- Der Aufbau laeuft ueber `innerHTML` in `render()`. Die globalen Handler `setMetric`, `toggleAll` und `saveManual` werden aus dem Markup heraus aufgerufen und muessen global bleiben.
- Jede per `getElementById` geholte ID muss im erzeugten Markup existieren, `tools/check_html.py` prueft das.
- Zielgeraet ist ein Handy, Viewport 390px. Nichts einbauen, das darunter umbricht oder horizontal scrollt.
- `lang="de"` im `html`-Tag bleibt, Zahlen bleiben in `de-DE`-Formatierung.
- Aenderungen nur mit `/dashboard-preview` pruefen und erst danach committen.
- Manuelle Werte bleiben im localStorage, sie gehoeren nicht ungefragt nach `docs/data.json`.
