"""Smoke test for the Zibbly planner page.

A README-only commit previously deployed over the shop and the domain 404ed.
This fails unless index.html is still the static catalog with its prices,
Etsy listing links, the 12-planner bundle, and the Christmas hero that
shows through 2026-12-15.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
VERCEL = ROOT / "vercel.json"

# name, price, Etsy listing id, optional badge
PLANNERS = [
    ("Budget Planner", "7.99", "4598975283", "Popular"),
    ("Cleaning Planner", "5.99", "4599103238", None),
    ("Moving Planner", "7.99", "4599146635", None),
    ("Wedding Planner", "12.99", "4599126511", None),
    ("Meal Planner", "5.99", "4599081891", None),
    ("Focus Daily Planner", "6.99", "4599122160", None),
    ("Fitness Planner", "7.99", "4599144707", None),
    ("2027 Planner", "6.99", "4599086021", "New year"),
    ("Christmas Planner", "7.99", "4599148952", "Holiday"),
    ("Travel Planner", "7.99", "4599127589", None),
    ("Reading Journal", "7.99", "4599128843", None),
    ("Small Business Planner", "9.99", "4599148289", None),
]


class StorefrontRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.vercel = VERCEL.read_text(encoding="utf-8")

    def test_static_file_has_no_build(self):
        self.assertTrue(INDEX.is_file())
        self.assertGreater(INDEX.stat().st_size, 1000)
        self.assertFalse((ROOT / "package.json").exists())

    def test_catalog_prices_and_listing_links(self):
        rows = re.findall(
            r'\["((?:\\.|[^"\\])*)","((?:\\.|[^"\\])*)","([0-9.]+)","(\d+)","([^"]+)"(?:,\"([^\"]+)\")?\]',
            self.html,
        )
        self.assertEqual(len(rows), 12)
        found = [(name, price, listing, badge or None) for name, _blurb, price, listing, _img, badge in rows]
        self.assertEqual(found, list(PLANNERS))
        total = round(sum(float(price) for _n, price, _i, _b in PLANNERS), 2)
        self.assertEqual(total, 96.88)
        self.assertIn("https://www.etsy.com/ca/listing/4599392487", self.html)
        self.assertIn("CA$34.99", self.html)
        self.assertIn("CA$96.88", self.html)
        self.assertIn("https://www.etsy.com/ca/shop/ZibblyStore", self.html)
        self.assertIn("https://i.etsystatic.com/68537175/r/il/", self.html)
        self.assertIn("https://www.etsy.com/ca/listing/'+p[3]+'", self.html)
        for _name, _price, listing, _badge in PLANNERS:
            self.assertIn(listing, self.html)

    def test_page_copy_and_policies(self):
        for phrase in (
            "Printable planners.",
            "Download in seconds.",
            "All 12 planners in one download",
            "200+ pages, Letter and A4.",
            "Nothing is shipped",
            "refunds and exchanges are not available",
            "Last updated October 20, 2026",
            "This website does not collect personal information",
            "no accounts, forms, cookies or analytics",
            'build(PLANNERS,"grid")',
        ):
            self.assertIn(phrase, self.html)

    def test_christmas_hero_through_dec_15_without_prices(self):
        self.assertLess(self.html.index('id="hero-christmas"'), self.html.index('id="bundle"'))
        self.assertLess(self.html.index('id="hero-default"'), self.html.index('id="bundle"'))
        hero = self.html.split('id="hero-christmas"', 1)[1].split('id="hero-default"', 1)[0]
        for phrase in (
            'data-show-through="2026-12-15"',
            "holiday pick",
            "christmas, planned on one page",
            "gift list, budget, card list, menu and countdown. download tonight, print at home.",
            "get the christmas planner on etsy",
            "https://www.etsy.com/listing/4599148952/christmas-planner-printable-holiday",
            "christmas + budget + meals bundle",
            "https://www.etsy.com/listing/4602671949/holiday-planner-bundle-christmas-planner",
        ):
            self.assertIn(phrase, hero)
        self.assertIn("SEASONAL-CHRISTMAS", self.html)
        self.assertIsNone(re.search(r"(CA\$|\$\s?\d|\d+\.\d{2}|\b20\s?%)", hero))
        self.assertRegex(self.html, r'<section class="hero" id="hero-default" hidden>')
        self.assertIn('id="hero-season"', self.html)
        self.assertIn('timeZone:"America/Toronto"', self.html)
        self.assertIn("fallback.hidden=false", self.html)
        bundle = self.html.split('id="bundle"', 1)[1].split('id="planners"', 1)[0]
        self.assertIn("All 12 planners in one download", bundle)
        self.assertIn("CA$34.99", bundle)
        self.assertIn("https://www.etsy.com/ca/listing/4599392487", bundle)

    def test_vercel_serves_static_root_and_skips_a_bad_commit(self):
        self.assertIn('"framework": null', self.vercel)
        self.assertIn('"buildCommand": null', self.vercel)
        self.assertIn('"installCommand": null', self.vercel)
        self.assertIn("tests/test_storefront.py", self.vercel)
        self.assertIn("&& exit 1 || exit 0", self.vercel)


if __name__ == "__main__":
    unittest.main()
