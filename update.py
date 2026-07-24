# ---------------------------------------------------------------
# Mission Control Autopilot - holt 1x taeglich die Profilzahlen
# und schreibt sie nach docs/data.json (fuer das Dashboard).
#
# >>> HIER deine Account-Namen eintragen (ohne @): <<<
HANDLES = {
    "tiktok": "spacefactswow",
    "youtube": "spacefactswow",   # dein YouTube-Handle
    "instagram": "spacefactswow",  # leer lassen = ueberspringen
}
# ---------------------------------------------------------------

import json
import re
import datetime
import pathlib
import urllib.request

DATA = pathlib.Path("docs/data.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Cookie": "CONSENT=YES+1",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def via_jina(url):
    # Kostenloser Lese-Proxy als Fallback, falls die Seite Bots blockt.
    return fetch("https://r.jina.ai/" + url, timeout=50)


def compact(s):
    """'1.2K' -> 1200, '3,456' -> 3456, '2.1M' -> 2100000"""
    m = re.match(r"([\d.,]+)\s*([KMB]?)", s.strip(), re.I)
    if not m:
        return None
    num, suf = m.group(1), m.group(2).upper()
    try:
        if suf:
            return int(float(num.replace(",", "")) * {"K": 1e3, "M": 1e6, "B": 1e9}[suf])
        n = re.sub(r"[^\d]", "", num)
        return int(n) if n else None
    except ValueError:
        return None


def grab(patterns, text):
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            v = compact(m.group(1))
            if v is not None:
                return v
    return None


def get_tiktok(h):
    out = {"f": None, "l": None}
    for getter in (lambda: fetch("https://www.tiktok.com/@" + h),
                   lambda: via_jina("https://www.tiktok.com/@" + h)):
        try:
            html = getter()
        except Exception:
            continue
        f = grab([r'"followerCount"\s*:\s*(\d+)',
                  r'([\d.,]+[KMB]?)\s*Follower'], html)
        l = grab([r'"heartCount"\s*:\s*(\d+)',
                  r'([\d.,]+[KMB]?)\s*Likes'], html)
        if f is not None:
            out = {"f": f, "l": l}
            break
    return out


def get_youtube(h):
    out = {"f": None, "v": None}
    for getter in (lambda: fetch("https://www.youtube.com/@" + h + "/about"),
                   lambda: via_jina("https://www.youtube.com/@" + h + "/about")):
        try:
            html = getter()
        except Exception:
            continue
        f = grab([r'([\d.,]+[KMB]?)\s*(?:subscribers|Abonnenten)',
                  r'"subscriberCountText"[^}]*?"simpleText"\s*:\s*"([\d.,KMB]+)'], html)
        v = grab([r'([\d.,]+)\s*(?:views|Aufrufe)'], html)
        if f is not None:
            out = {"f": f, "v": v}
            break
    return out


def get_instagram(h):
    if not h:
        return {"f": None}
    # 1) JSON-Endpunkt (zuverlaessigster Weg)
    try:
        req = urllib.request.Request(
            "https://i.instagram.com/api/v1/users/web_profile_info/?username=" + h,
            headers={"User-Agent": UA, "x-ig-app-id": "936619743392459",
                     "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"})
        with urllib.request.urlopen(req, timeout=25) as r:
            j = json.loads(r.read().decode("utf-8", "ignore"))
        f = j.get("data", {}).get("user", {}).get("edge_followed_by", {}).get("count")
        if isinstance(f, int):
            return {"f": f}
    except Exception:
        pass
    # 2) Profilseite, 3) Lese-Proxy
    for getter in (lambda: fetch("https://www.instagram.com/" + h + "/"),
                   lambda: via_jina("https://www.instagram.com/" + h + "/")):
        try:
            html = getter()
        except Exception:
            continue
        f = grab([r'([\d.,]+[KMB]?)\s*Follower'], html)
        if f is not None:
            return {"f": f}
    return {"f": None}


def merge(old, new):
    """Neue Werte gewinnen, aber None ueberschreibt keine guten alten Werte."""
    if not old:
        return new
    keys = set(old) | set(new)
    return {k: (new.get(k) if new.get(k) is not None else old.get(k)) for k in keys}


def main():
    today = datetime.date.today().isoformat()

    data = {"entries": []}
    if DATA.exists():
        try:
            data = json.loads(DATA.read_text())
        except Exception:
            pass
    entries = data.get("entries", [])
    old_today = next((e for e in entries if e.get("date") == today), None)

    tt = get_tiktok(HANDLES["tiktok"]) if HANDLES["tiktok"] else {"f": None, "l": None}
    yt = get_youtube(HANDLES["youtube"]) if HANDLES["youtube"] else {"f": None, "v": None}
    ig = get_instagram(HANDLES["instagram"])

    entry = {
        "date": today,
        "tiktok": merge(old_today.get("tiktok") if old_today else None, tt),
        "youtube": merge(old_today.get("youtube") if old_today else None, yt),
        "instagram": merge(old_today.get("instagram") if old_today else None, ig),
    }

    entries = [e for e in entries if e.get("date") != today]
    entries.append(entry)
    entries.sort(key=lambda e: e.get("date", ""))

    out = {
        "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "handles": HANDLES,
        "entries": entries[-400:],
    }
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("OK:", json.dumps(entry, ensure_ascii=False))


if __name__ == "__main__":
    main()
