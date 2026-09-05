#!/usr/bin/env python3
"""Prueft docs/data.json gegen das Schema aus CLAUDE.md.

Aufruf:  python3 tools/check_data.py [--today]
--today prueft zusaetzlich, ob der heutige UTC-Eintrag da ist und TikTok geliefert hat.
Exit 0 = alles in Ordnung, Exit 1 = Fehler (eine Zeile pro Fehler auf stderr).
"""
import datetime
import json
import pathlib
import sys

DATA = pathlib.Path(__file__).resolve().parents[1] / "docs" / "data.json"
MAX_ENTRIES = 400
REQUIRED = {"tiktok": ("f", "l"), "youtube": ("f", "v"), "instagram": ("f",)}


def is_value(v):
    """int oder None, aber kein bool und kein String."""
    return v is None or (isinstance(v, int) and not isinstance(v, bool))


def check(data):
    errors = []
    entries = data.get("entries")
    if not isinstance(entries, list):
        return ["entries fehlt oder ist keine Liste"]
    if len(entries) > MAX_ENTRIES:
        errors.append("zu viele Eintraege: %d (max %d)" % (len(entries), MAX_ENTRIES))

    seen = set()
    last_date = ""
    for i, e in enumerate(entries):
        where = "Eintrag %d" % i
        if not isinstance(e, dict):
            errors.append("%s ist kein Objekt" % where)
            continue
        date = e.get("date")
        if not isinstance(date, str):
            errors.append("%s: date fehlt oder ist kein String" % where)
        else:
            where = "Eintrag %s" % date
            try:
                datetime.date.fromisoformat(date)
            except ValueError:
                errors.append("%s: date ist kein Datum im Format YYYY-MM-DD" % where)
            if date in seen:
                errors.append("%s: Datum kommt mehrfach vor" % where)
            seen.add(date)
            if date < last_date:
                errors.append("%s: Datum steht nicht aufsteigend (nach %s)" % (where, last_date))
            last_date = max(last_date, date)

        for platform, keys in REQUIRED.items():
            block = e.get(platform)
            if not isinstance(block, dict):
                errors.append("%s: %s fehlt oder ist kein Objekt" % (where, platform))
                continue
            for k in keys:
                if k not in block:
                    errors.append("%s: %s.%s fehlt" % (where, platform, k))
                elif not is_value(block[k]):
                    errors.append("%s: %s.%s ist weder int noch null (%r)"
                                  % (where, platform, k, block[k]))
            # Zusaetzliche Schluessel sind erlaubt, muessen aber denselben Typ haben.
            for k, v in block.items():
                if k not in keys and not is_value(v):
                    errors.append("%s: %s.%s ist weder int noch null (%r)"
                                  % (where, platform, k, v))
    return errors


def check_today(entries):
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    if not entries:
        return ["keine Eintraege vorhanden"]
    last = entries[-1]
    if last.get("date") != today:
        return ["letzter Eintrag ist %s, erwartet %s (Abruf ausgefallen?)"
                % (last.get("date"), today)]
    if (last.get("tiktok") or {}).get("f") is None:
        return ["Eintrag %s hat keine TikTok-Follower (Abruf gescheitert)" % today]
    return []


def main():
    strict_today = "--today" in sys.argv[1:]
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("FEHLER: %s nicht gefunden" % DATA, file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print("FEHLER: kein gueltiges JSON (%s)" % exc, file=sys.stderr)
        return 1

    errors = check(data)
    if strict_today and not errors:
        errors += check_today(data.get("entries") or [])

    if errors:
        for e in errors:
            print("FEHLER: " + e, file=sys.stderr)
        print("check_data: %d Fehler" % len(errors))
        return 1
    print("check_data: OK, %d Eintraege, letzter %s"
          % (len(data["entries"]), data["entries"][-1]["date"] if data["entries"] else "keiner"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
