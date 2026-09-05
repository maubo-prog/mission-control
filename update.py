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


def parse_tiktok(html):
    """Follower und Likes aus der Profilseite.

    TikTok liefert zwei Bloecke: "stats" mit gerundeten Zahlen (13500) und
    "statsV2" mit exakten Werten als String ("13483"). statsV2 kommt zuerst,
    danach der alte Weg ueber "stats" und zuletzt der sichtbare Text.
    """
    f = grab([r'"statsV2"\s*:\s*\{[^}]*?"followerCount"\s*:\s*"(\d+)"',
              r'"followerCount"\s*:\s*(\d+)',
              r'([\d.,]+[KMB]?)\s*Follower'], html)
    l = grab([r'"statsV2"\s*:\s*\{[^}]*?"heartCount"\s*:\s*"(\d+)"',
              r'"heartCount"\s*:\s*(\d+)',
              r'([\d.,]+[KMB]?)\s*Likes'], html)
    return {"f": f, "l": l}


def get_tiktok(h):
    out = {"f": None, "l": None}
    for getter in (lambda: fetch("https://www.tiktok.com/@" + h),
                   lambda: via_jina("https://www.tiktok.com/@" + h)):
        try:
            html = getter()
        except Exception as e:
            print("TikTok: Abruf fehlgeschlagen:", repr(e))
            continue
        parsed = parse_tiktok(html)
        if parsed["f"] is not None:
            out = parsed
            break
    return out


# Die Kanalseite nennt die Gesamtaufrufe nicht mehr, nur noch die Aufrufe je
# Video. Deshalb werden Videos- und Shorts-Tab durchgeblaettert und summiert.
YT_TABS = (("videos", "EgZ2aWRlb3PyBgQKAjoA"), ("shorts", "EgZzaG9ydHPyBgUKA5oBAA=="))
YT_MAX_PAGES = 10


def yt_config(html):
    """Liest API-Schluessel, Kanal-ID und Client-Version aus der Kanalseite."""
    key = re.search(r'"INNERTUBE_API_KEY"\s*:\s*"([^"]+)"', html)
    channel = re.search(r'"(?:externalId|browseId)"\s*:\s*"(UC[\w-]{20,})"', html)
    version = re.search(r'"INNERTUBE_CLIENT_VERSION"\s*:\s*"([^"]+)"', html)
    if not (key and channel and version):
        return None
    return {"key": key.group(1), "channel": channel.group(1), "version": version.group(1)}


def yt_browse(cfg, payload, timeout=25):
    """Ein Aufruf der oeffentlichen Browse-Schnittstelle, gibt den Rohtext zurueck."""
    body = {"context": {"client": {"clientName": "WEB", "clientVersion": cfg["version"],
                                   "hl": "en", "gl": "US"}}}
    body.update(payload)
    req = urllib.request.Request(
        "https://www.youtube.com/youtubei/v1/browse?key=" + cfg["key"] + "&prettyPrint=false",
        data=json.dumps(body).encode("utf-8"),
        headers={"User-Agent": UA, "Content-Type": "application/json",
                 "Accept-Language": "en-US,en;q=0.9", "Cookie": "CONSENT=YES+1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def yt_views(raw):
    """Alle Aufrufzahlen einer Antwort. '1.1K views' zaehlt gerundet mit."""
    werte = [compact(s) for s in re.findall(r'"([\d.,]+[KMB]?) views"', raw)]
    return [w for w in werte if w is not None]


def yt_continuation(raw):
    """Token fuer die naechste Seite, None am Ende der Liste."""
    m = re.search(r'"continuationCommand"\s*:\s*\{"token"\s*:\s*"([^"]+)"', raw)
    return m.group(1) if m else None


def yt_subscribers(raw):
    return grab([r'"([\d.,]+[KMB]?) subscribers"',
                 r'([\d.,]+[KMB]?)\s*(?:subscribers|Abonnenten)',
                 r'"subscriberCountText"[^}]*?"simpleText"\s*:\s*"([\d.,KMB]+)'], raw)


def get_youtube(h):
    out = {"f": None, "v": None}
    html = ""
    for getter in (lambda: fetch("https://www.youtube.com/@" + h + "?hl=en"),
                   lambda: via_jina("https://www.youtube.com/@" + h)):
        try:
            html = getter()
            break
        except Exception as e:
            print("YouTube: Kanalseite nicht erreichbar:", repr(e))
    if html:
        out["f"] = yt_subscribers(html)

    cfg = yt_config(html) if html else None
    if not cfg:
        print("YouTube: kein Zugang zur Browse-Schnittstelle, Aufrufe bleiben leer")
        return out

    summe, gezaehlt = 0, 0
    for tab, params in YT_TABS:
        payload = {"browseId": cfg["channel"], "params": params}
        for seite in range(YT_MAX_PAGES):
            try:
                raw = yt_browse(cfg, payload)
            except Exception as e:
                # Eine halbe Summe waere schlechter als gar keine.
                print("YouTube: %s Seite %d fehlgeschlagen: %r" % (tab, seite + 1, e))
                return out
            werte = yt_views(raw)
            summe += sum(werte)
            gezaehlt += len(werte)
            if out["f"] is None:
                out["f"] = yt_subscribers(raw)
            token = yt_continuation(raw)
            if not token:
                break
            payload = {"continuation": token}

    if gezaehlt:
        out["v"] = summe
    else:
        print("YouTube: keine Aufrufzahlen in der Antwort gefunden")
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
