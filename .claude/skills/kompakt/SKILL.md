---
name: kompakt
description: Fasst in fuenf Zeilen zusammen, was aus dem laufenden Kontext behalten werden muss, und liefert den fertigen Fokus-Text fuer /compact. Aendert nichts, nur auf ausdruecklichen Aufruf.
disable-model-invocation: true
allowed-tools: Bash
---
# Kontext vorbereiten

Zweck: vor `/compact` festhalten, was sonst verloren geht. Diese Skill aendert keine Datei
und committet nichts.

## Ablauf

1. `git branch --show-current` und `git status --short` ausfuehren, mehr nicht.
2. Fuenf Zeilen ausgeben, jede mit einem konkreten Fakt:
   - Branch und ob etwas uncommittet ist
   - welche Dateien in dieser Session geaendert wurden
   - welche Entscheidung offen ist und welche Optionen im Raum stehen
   - welcher Befehl zuletzt gruen oder rot war
   - was der naechste Schritt ist
3. Danach den fertigen Befehl zum Kopieren ausgeben, als eine Zeile:

   `/compact <ein Satz, der die fuenf Punkte zusammenfasst>`

## Regeln

- Keine Code-Ausschnitte in die Zusammenfassung, nur Dateinamen und Zeilennummern.
- Keine Datei zusaetzlich lesen, um die Zusammenfassung zu schreiben. Was nicht im Kontext ist,
  gehoert nicht hinein.
- Wenn die Session ohnehin am Ende ist, stattdessen `/handoff` empfehlen. `/compact` behaelt
  Kontext fuer dieselbe Session, `/handoff` uebergibt an die naechste.
