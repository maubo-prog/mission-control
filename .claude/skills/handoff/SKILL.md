---
name: handoff
description: Schreibt die Session-Uebergabe in .claude/handoff.md neu und committet sie, damit die naechste Session ohne Nachfragen weiterarbeiten kann. Nur auf ausdruecklichen Aufruf.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash
---
# Uebergabe schreiben

## Ablauf

1. Stand sammeln: `git branch --show-current`, `git status --short`, `git log --oneline -5`.
2. `.claude/handoff.md` **ersetzen**, nicht ergaenzen. Maximal 40 Zeilen. Alte Inhalte fliegen raus,
   die Datei ist eine Momentaufnahme, kein Protokoll.
3. Diese Abschnitte fuellen, jeweils mit Stichpunkten:
   - **Erledigt**: was in dieser Session fertig wurde, mit Dateinamen
   - **Offen**: was angefangen oder bewusst liegen geblieben ist, mit Grund
   - **Naechster Schritt**: genau ein konkreter Schritt, mit dem die naechste Session anfaengt
   - **Geprueft**: die tatsaechlich gelaufenen Befehle mit Ergebnis, keine Absichtserklaerungen
   - **Branch und offene PRs**: Branch-Name und PR-Link
4. Den Hinweisblock oben in der Datei stehen lassen (Import, Branch-Bindung, 40-Zeilen-Grenze).
5. Committen: `git add .claude/handoff.md` und `git commit -m "Doku: Uebergabe <kurzes Thema>"`.
   Wenn noch anderes uncommittet ist, vorher fragen, ob das mit soll.
6. Falls der Branch noch nicht gepusht ist: `git push -u origin <branch>`.

## Am Ende im Chat nennen

- Branch-Name (den braucht die naechste Web-Session beim Anlegen)
- PR-Link, falls vorhanden
- Hinweis: die Uebergabe liegt auf dem `claude/`-Branch und ist auf main erst nach dem Merge sichtbar
- Empfehlung fuer den Neustart:
  - CLI: `/clear`, danach `/briefing`
  - Web: neue Session aus der Seitenleiste, beim Anlegen denselben Branch waehlen
  - Wenn der Verlauf noch gebraucht wird: `/kompakt`, danach `/compact <fokus>`
