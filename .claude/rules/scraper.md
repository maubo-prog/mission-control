---
paths: ["update.py", "tests/**"]
---

# Regeln fuer den Abruf

- Beim Umbau Laden und Parsen trennen: eine Funktion holt HTML, eine liest Zahlen daraus. Nur so ist der Parser testbar.
- Erst strukturiert parsen (JSON-Block im HTML), Regex nur als Fallback. Alte Regex als zweiten Versuch stehen lassen.
- Jede Aenderung am Parser braucht einen Test gegen eine gespeicherte Fixture unter `tests/fixtures/`, kein Live-Trial-and-Error.
- Exceptions nicht still schlucken: der Abruf darf scheitern und null liefern, aber der Grund gehoert in die Ausgabe.
- `merge()` und die Schluessel `f`, `l`, `v` nicht aendern, `docs/index.html` haengt daran.
- Keine neuen Abhaengigkeiten, nur `urllib`, `re`, `json`, `datetime`, `pathlib`.
- Fixtures vor dem Commit von Cookies und Tokens befreien und auf unter 50 KB kuerzen.
