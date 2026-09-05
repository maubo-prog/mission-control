---
name: scraper-fix
description: Repariert einen ausgefallenen Abruf in update.py (TikTok, YouTube, Instagram) anhand gespeicherter HTML-Fixtures statt Live-Versuchen. Nutzen, wenn data.json null oder unplausible Werte zeigt.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---
# Scraper reparieren

## Ablauf

1. Symptom festhalten: `python3 tools/stats.py --days 7`.
2. Fixture holen, genau einmal: `python3 -c "import urllib.request;r=urllib.request.Request('https://www.tiktok.com/@spacefactswow',headers={'User-Agent':'Mozilla/5.0'});open('tests/fixtures/tiktok_$(date +%F).html','wb').write(urllib.request.urlopen(r,timeout=25).read())"` (Plattform und URL anpassen, fragt nach Erlaubnis). Cookies oder Tokens im Fixture schwaerzen, Datei auf die relevanten Ausschnitte kuerzen (unter 50 KB).
3. Zielzahl im Fixture lokalisieren: `grep -o '"followerCount":[0-9]*' tests/fixtures/...` bzw. `grep -n -i 'Follower' ...`. Nie die ganze Datei mit Read oeffnen.
4. In `update.py` den Parser anpassen. Reihenfolge: JSON-Block parsen (z. B. `__UNIVERSAL_DATA_FOR_REHYDRATION__`) vor Regex, alte Regex als Fallback behalten. `merge()` und die Schluessel `f`, `l`, `v` nicht aendern.
5. Test in `tests/test_update.py` ergaenzen, der das Fixture liest und den erwarteten Wert prueft. `python3 -m unittest discover -s tests -v` muss gruen sein.
6. Erst jetzt ein einziger Live-Lauf: `python3 update.py` (fragt nach Erlaubnis). Ausgabe pruefen, dann `git checkout docs/data.json`.
7. Commit `Fix: <Plattform>-Abruf repariert (<was>)`, dann `/pr`.

## Regeln

- Keine neuen Abhaengigkeiten, nur `urllib`, `re`, `json`.
- Keine Schleifen gegen die Live-Seite, jede Iteration laeuft gegen das Fixture.
- Wenn eine Plattform Login verlangt (Instagram): nicht umgehen, sondern im Bericht als "manuell" vorschlagen. Der Weg dafuer ist das Issue-Formular "Zahlen nachtragen" plus `/data-repair`.
