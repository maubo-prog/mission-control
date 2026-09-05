---
name: wochenbericht
description: Schreibt aus tools/stats.py einen deutschen Wochenbericht zur Mission mit Deltas, Tempo, Prognose und drei Content-Hinweisen. Nutzen bei "Wochenbericht", "wie laeuft die Mission", montags.
allowed-tools: Read, Write, Bash
---
# Wochenbericht

## Ablauf

1. Zahlen holen, ausschliesslich so: `python3 tools/stats.py --days 30`.
   `docs/data.json` nicht oeffnen, Read darauf ist gesperrt.
2. Bericht schreiben, deutsch, du-Form, maximal 25 Zeilen, in dieser Reihenfolge:
   - **Stand**: Follower je Plattform, TikTok zuerst
   - **Woche**: Delta 7 Tage, daneben Delta 30 Tage zum Vergleich
   - **Tempo**: Follower pro Tag, gesamt und aus den letzten 14 Tagen
   - **Prognose 10k**: beide Datumsangaben nennen und sagen, welche realistischer ist
   - **Beste und schwaechste Tage** im Fenster
   - **Datenluecken**: Tage ohne Wert, mit dem Hinweis, dass Instagram grundsaetzlich fehlt
   - **Drei Content-Hinweise**: konkret und aus den Zahlen abgeleitet, keine Allgemeinplaetze
3. Auf Wunsch als Datei ablegen: `reports/YYYY-WW.md`. Vorher darauf hinweisen, dass das Repo
   oeffentlich ist und der Bericht damit fuer jeden lesbar wird. Danach `/pr`.

## Regeln

- Keine Zahl erfinden und keine schaetzen. Was `stats.py` nicht liefert, steht nicht im Bericht.
- YouTube-Views immer als unzuverlaessig kennzeichnen, die Regex greift ein Einzelvideo.
- TikTok-Views aus dem Handy-localStorage liegen nicht im Repo und fehlen deshalb im Bericht.
- Bei negativem oder sehr kleinem Tempo die Prognose nicht schoenrechnen, sondern das offen sagen.
- Die Content-Hinweise beziehen sich auf Zahlen, nicht auf Produktionsdetails. Die Videoarbeit
  laeuft ueber die Konto-Skills und einen eigenen Auftrag, nicht ueber dieses Repo.
