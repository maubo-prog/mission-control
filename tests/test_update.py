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


if __name__ == "__main__":
    unittest.main()
