#!/usr/bin/env python3
"""Kennzahlen aus docs/data.json, ohne die Datei in den Kontext zu holen.

Aufruf:  python3 tools/stats.py [--days N] [--json]
Standard sind 30 Tage. Die Textausgabe bleibt unter 40 Zeilen.
"""
import argparse
import datetime
import json
import pathlib
import sys

DATA = pathlib.Path(__file__).resolve().parents[1] / "docs" / "data.json"
GOAL_FOLLOWERS = 10000
PLATFORMS = (("tiktok", "f", "TikTok-Follower"),
             ("tiktok", "l", "TikTok-Likes"),
             ("youtube", "f", "YouTube-Abos"),
             ("youtube", "v", "YouTube-Views (unzuverlaessig, Regex greift ein Einzelvideo)"),
             ("instagram", "f", "Instagram-Follower"))


def value(entry, platform, key):
    block = entry.get(platform) or {}
    v = block.get(key)
    return v if isinstance(v, int) and not isinstance(v, bool) else None


def days_between(a, b):
    return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days


def series(entries, platform, key):
    """Nur Tage mit echtem Wert, als Liste von (datum, wert)."""
    out = []
    for e in entries:
        v = value(e, platform, key)
        if v is not None and isinstance(e.get("date"), str):
            out.append((e["date"], v))
    return out


def delta_over(points, window):
    """Veraenderung ueber die letzten `window` Tage, gemessen am juengsten Punkt."""
    if len(points) < 2:
        return None, None
    last_date, last_value = points[-1]
    cutoff = (datetime.date.fromisoformat(last_date)
              - datetime.timedelta(days=window)).isoformat()
    base = None
    for d, v in points:
        if d <= cutoff:
            base = (d, v)
    if base is None:
        base = points[0]
    if base[0] == last_date:
        return None, None
    return last_value - base[1], days_between(base[0], last_date)


def forecast(points, window=None):
    """Datum, an dem 10k erreicht waeren, linear aus dem gewaehlten Fenster."""
    pts = points
    if window is not None and points:
        cutoff = (datetime.date.fromisoformat(points[-1][0])
                  - datetime.timedelta(days=window)).isoformat()
        pts = [p for p in points if p[0] >= cutoff]
    if len(pts) < 2:
        return None, None
    span = days_between(pts[0][0], pts[-1][0])
    if span <= 0:
        return None, None
    pace = (pts[-1][1] - pts[0][1]) / span
    if pace <= 0:
        return pace, None
    missing = GOAL_FOLLOWERS - pts[-1][1]
    if missing <= 0:
        return pace, pts[-1][0]
    target = datetime.date.fromisoformat(pts[-1][0]) + datetime.timedelta(days=missing / pace)
    return pace, target.isoformat()


def daily_changes(points):
    out = []
    for (d1, v1), (d2, v2) in zip(points, points[1:]):
        span = days_between(d1, d2)
        if span > 0:
            out.append((d2, (v2 - v1) / span))
    return out


def collect(entries, days):
    cutoff = None
    if entries:
        last = entries[-1].get("date")
        if isinstance(last, str):
            cutoff = (datetime.date.fromisoformat(last)
                      - datetime.timedelta(days=days)).isoformat()
    window = [e for e in entries if not cutoff or e.get("date", "") >= cutoff]

    result = {"days": days, "entries_total": len(entries),
              "entries_window": len(window), "platforms": {}, "gaps": {}}
    if entries:
        result["first"] = entries[0].get("date")
        result["last"] = entries[-1].get("date")

    for platform, key, label in PLATFORMS:
        points = series(entries, platform, key)
        name = "%s.%s" % (platform, key)
        d7, span7 = delta_over(points, 7)
        d30, span30 = delta_over(points, 30)
        info = {"label": label,
                "last": points[-1][1] if points else None,
                "last_date": points[-1][0] if points else None,
                "delta_7": d7, "delta_7_days": span7,
                "delta_30": d30, "delta_30_days": span30}
        if platform == "tiktok" and key == "f":
            pace_all, date_all = forecast(points)
            pace_14, date_14 = forecast(points, 14)
            info["pace_all"] = pace_all
            info["goal_date_all"] = date_all
            info["pace_14"] = pace_14
            info["goal_date_14"] = date_14
            changes = daily_changes([p for p in points if p[0] >= (cutoff or "")])
            if changes:
                best = max(changes, key=lambda c: c[1])
                worst = min(changes, key=lambda c: c[1])
                info["best_day"] = {"date": best[0], "change": round(best[1], 1)}
                info["worst_day"] = {"date": worst[0], "change": round(worst[1], 1)}
        result["platforms"][name] = info
        result["gaps"][name] = [e["date"] for e in window
                                if value(e, platform, key) is None and e.get("date")]
    return result


def number(v):
    return "-" if v is None else format(int(round(v)), ",").replace(",", ".")


def signed(v, span):
    if v is None:
        return "-"
    return "%+d%s" % (round(v), "" if span is None else " (%d Tage)" % span)


def report(r):
    lines = []
    lines.append("Datenstand %s bis %s, %d Eintraege, Fenster %d Tage"
                 % (r.get("first", "?"), r.get("last", "?"), r["entries_total"], r["days"]))
    lines.append("")
    lines.append("Kennzahl                     aktuell     7 Tage    30 Tage")
    for platform, key, label in PLATFORMS:
        info = r["platforms"]["%s.%s" % (platform, key)]
        short = label.split(" (")[0]
        lines.append("%-26s %9s %10s %10s"
                     % (short, number(info["last"]),
                        signed(info["delta_7"], None), signed(info["delta_30"], None)))
    lines.append("")

    tt = r["platforms"]["tiktok.f"]
    if tt["last"] is not None:
        rest = GOAL_FOLLOWERS - tt["last"]
        lines.append("Mission 10k: %s von 10.000, es fehlen %s (%.0f Prozent geschafft)"
                     % (number(tt["last"]), number(rest), tt["last"] / GOAL_FOLLOWERS * 100))
    if tt.get("pace_all"):
        lines.append("Tempo gesamt: %+.1f Follower pro Tag, 10k am %s"
                     % (tt["pace_all"], tt.get("goal_date_all") or "nie bei diesem Tempo"))
    if tt.get("pace_14"):
        lines.append("Tempo letzte 14 Tage: %+.1f pro Tag, 10k am %s"
                     % (tt["pace_14"], tt.get("goal_date_14") or "nie bei diesem Tempo"))
    if tt.get("best_day"):
        lines.append("Bester Tag: %s mit %+.0f, schwaechster Tag: %s mit %+.0f"
                     % (tt["best_day"]["date"], tt["best_day"]["change"],
                        tt["worst_day"]["date"], tt["worst_day"]["change"]))
    lines.append("")
    lines.append("Luecken im Fenster (Tage ohne Wert):")
    for platform, key, label in PLATFORMS:
        gaps = r["gaps"]["%s.%s" % (platform, key)]
        short = label.split(" (")[0]
        if not gaps:
            lines.append("  %-24s keine" % short)
        elif len(gaps) > 6:
            lines.append("  %-24s %d Tage, u.a. %s" % (short, len(gaps), ", ".join(gaps[:4])))
        else:
            lines.append("  %-24s %s" % (short, ", ".join(gaps)))
    lines.append("")
    lines.append("Hinweis: YouTube-Views sind unzuverlaessig (Regex greift ein Einzelvideo).")
    lines.append("Instagram liefert seit Beginn null, TikTok-Likes sind seit 12.08. auf 100er gerundet.")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Kennzahlen aus docs/data.json")
    p.add_argument("--days", type=int, default=30, help="Fenster in Tagen (Standard 30)")
    p.add_argument("--json", action="store_true", help="Rohdaten als JSON ausgeben")
    args = p.parse_args()

    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print("FEHLER: docs/data.json nicht lesbar (%s)" % exc, file=sys.stderr)
        return 1

    entries = [e for e in data.get("entries", []) if isinstance(e, dict)]
    entries.sort(key=lambda e: e.get("date", ""))
    result = collect(entries, args.days)
    result["updated"] = data.get("updated")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print(report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
