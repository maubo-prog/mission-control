# Routinen auf Claude Code Web

Routinen laufen in der Cloud ohne Rueckfragen und verbrauchen Kontingent. In diesem Repo ist
deshalb genau eine sinnvoll. Anlegen tust du sie selbst unter claude.ai/code/routines oder
in der CLI mit `/schedule`. Hier steht nur der fertige Vorschlag.

## Empfohlen: Wochenbericht

- **Zeitpunkt**: montags 07:00 Ortszeit. Im Web-Formular das Wochen-Preset waehlen, das rechnet
  die Zeitzone selbst um und braucht keinen eigenen Cron.
- Nur falls du doch einen eigenen Cron ueber `/schedule update` setzt: `0 5 * * 1` (Sommerzeit)
  bzw. `0 6 * * 1` (Winterzeit). Ob die Cron-Angabe dort in UTC oder Ortszeit gilt, ist nicht belegt.
- **Repository**: maubo-prog/mission-control
- **Connector**: nur GitHub, nichts weiter
- **Haeufigkeit**: eine Ausfuehrung pro Woche
- **Prompt**:

```
Fuehre /wochenbericht aus, schreibe reports/YYYY-WW.md auf Branch claude/report-YYYY-WW
und oeffne einen PR mit deutscher Zusammenfassung von max. 15 Zeilen. Kein Push auf main.
```

## Bewusst nicht angelegt

- **Taeglicher Stats-Waechter als Routine.** Macht `.github/workflows/watchdog.yml` gratis und
  ohne Kontingent, inklusive Alarm-Issue und Handy-Benachrichtigung.
- **`/loop` in einer Web-Session zur Dauerueberwachung.** Der Kontext waechst mit jeder Iteration,
  das frisst Kontingent, ohne mehr zu leisten als der Watchdog.

## Gut zu wissen

Routine-Trigger fuer GitHub-Ereignisse gibt es nur fuer Pull Request und Release, nicht fuer Issues.
Ein Issue aus dem Formular "Zahlen nachtragen" startet also nichts von selbst. Das ist Absicht:
du rufst `/data-repair` auf, wenn es dir passt.
