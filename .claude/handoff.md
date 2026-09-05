# Session-Uebergabe

Wird zu jedem Sessionstart geladen (Import in `CLAUDE.md`). Liegt auf dem `claude/`-Branch und ist
auf main erst nach dem Merge sichtbar, bis dahin naechste Web-Session auf denselben Branch stellen.
Schreiben nur ueber `/handoff` (ersetzt den Inhalt, haengt nichts an). Maximal 40 Zeilen.

## Erledigt

- YouTube-Views (`update.py`): YouTube nennt die Kanalsumme nirgends mehr. `get_youtube` blaettert
  Videos- und Shorts-Tab ueber die Browse-Schnittstelle und summiert. Laden und Parsen getrennt
  (`yt_config`, `yt_browse`, `yt_views`, `yt_continuation`, `yt_subscribers`). PR 6.
- TikTok-Likes (`update.py`): `parse_tiktok` liest `statsV2` (exakt) vor `stats` (gerundet). PR 8.
- Instagram: vom Runner geprueft, 429 und 403 ueberall, Embed ohne Zahl. Bleibt manuell, `CLAUDE.md`. PR 7.
- Hinweistexte in `tools/stats.py` und `.claude/skills/wochenbericht/SKILL.md` angepasst. PR 9.
- `docs/data.json`: `youtube.v` in allen 44 Eintraegen bis 05.09. auf null (`/data-repair`). PR 10.
- Fixtures `tests/fixtures/youtube_videos_`, `youtube_shorts_`, `tiktok_profile_2026-09-05`, Tests 7 auf 20.

## Offen

- Session-Umgebung ("trusted network") blockt youtube.com, tiktok.com, instagram.com, r.jina.ai.
  Live-Pruefungen liefen ueber einen temporaeren Workflow auf dem Runner, danach geloescht.
- YouTube-Views sind seit 06.09. eine Summe gerundeter Einzelwerte, etwa ein Prozent genau.
- TikTok-Likes 12.08. bis 05.09. bleiben gerundet in `data.json`, nicht reparabel.
- Manuell beim Betreiber: Branch-Schutz Variante A auf main. Label `zahlen` legt `watchdog.yml` selbst an.

## Naechster Schritt

- Am 06.09. `python3 tools/stats.py --days 3`: Eintrag 2026-09-06 mit `youtube.v` um 273.000 und
  exaktem `tiktok.l` erwartet. Fehlt er oder null: Lauf von `update.yml` in Actions, Logs an `pruefer`.

## Geprueft

- `py_compile update.py` OK, `unittest discover -s tests` 20 Tests OK.
- `tools/check_data.py` OK (44 Eintraege), `tools/check_html.py` OK (7 IDs), `stats.py --days 7` OK.
- Live auf dem Runner: `get_youtube` gibt `{'f': 583, 'v': 273290}`, `get_tiktok` gibt `{'f': 2872, 'l': 13483}`.
- CI gruen auf PR 6 bis 10. `update.yml` und `HANDLES` unveraendert.

## Branch und offene PRs

- Branch: claude/briefing-h9gjow, frisch von main nach Merge von PR 10 (614633b). Keine offenen PRs.
