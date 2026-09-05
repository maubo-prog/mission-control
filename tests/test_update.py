"""Tests fuer die reinen Funktionen aus update.py. Kein Netzzugriff.

`main()` haengt hinter `if __name__ == "__main__"`, der Import ist also gefahrlos.
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import update  # noqa: E402


class TestCompact(unittest.TestCase):
    def test_tausender_mit_k(self):
        self.assertEqual(update.compact("1.2K"), 1200)

    def test_komma_als_tausendertrenner(self):
        self.assertEqual(update.compact("3,456"), 3456)

    def test_millionen(self):
        self.assertEqual(update.compact("2.1M"), 2100000)

    def test_text_ergibt_none(self):
        self.assertIsNone(update.compact("abc"))


class TestMerge(unittest.TestCase):
    def test_none_ueberschreibt_guten_wert_nicht(self):
        self.assertEqual(update.merge({"f": 10, "l": 5}, {"f": None, "l": 7}),
                         {"f": 10, "l": 7})

    def test_ohne_alten_eintrag_gewinnt_der_neue(self):
        self.assertEqual(update.merge(None, {"f": 1}), {"f": 1})


class TestGrab(unittest.TestCase):
    def test_findet_followercount_im_json(self):
        self.assertEqual(update.grab([r'"followerCount":(\d+)'], '{"followerCount":42}'), 42)


FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def fixture(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


class TestYoutubeParser(unittest.TestCase):
    """Gegen echte, gekuerzte Antworten vom 05.09.2026."""

    def setUp(self):
        self.videos = fixture("youtube_videos_2026-09-05.json")
        self.shorts = fixture("youtube_shorts_2026-09-05.json")

    def test_aufrufe_aus_dem_videos_tab(self):
        self.assertEqual(update.yt_views(self.videos), [77])

    def test_aufrufe_aus_dem_shorts_tab_mit_gerundeten_werten(self):
        self.assertEqual(update.yt_views(self.shorts), [342, 509, 569])

    def test_abos_kommen_aus_der_antwort(self):
        self.assertEqual(update.yt_subscribers(self.videos), 583)

    def test_gerundete_angabe_wird_umgerechnet(self):
        self.assertEqual(update.yt_views('"1.1K views" "4.7K views"'), [1100, 4700])

    def test_einzelnes_video_ist_nicht_die_kanalsumme(self):
        # Der alte Parser nahm die erste Zahl vor "views", das war ein Einzelvideo.
        alt = update.grab([r'([\d.,]+)\s*(?:views|Aufrufe)'], self.videos)
        self.assertEqual(alt, 77)
        self.assertGreater(sum(update.yt_views(self.videos + self.shorts)), alt)

    def test_naechste_seite_wird_erkannt(self):
        self.assertIsNotNone(update.yt_continuation(self.shorts))
        self.assertIsNone(update.yt_continuation('{"contents":[]}'))

    def test_config_ohne_schluessel_ergibt_none(self):
        self.assertIsNone(update.yt_config("<html>nichts</html>"))

    def test_config_liest_kanal_und_version(self):
        html = ('"INNERTUBE_API_KEY":"AIzaTEST","externalId":"UC44N0a0qG1L8hCrh0x9OwDQ",'
                '"INNERTUBE_CLIENT_VERSION":"2.20260904.01.00"')
        cfg = update.yt_config(html)
        self.assertEqual(cfg["channel"], "UC44N0a0qG1L8hCrh0x9OwDQ")
        self.assertEqual(cfg["version"], "2.20260904.01.00")


if __name__ == "__main__":
    unittest.main()
