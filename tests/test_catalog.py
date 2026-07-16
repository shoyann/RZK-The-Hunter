import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from cataloglib import load_catalog, score_tool


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT / 'references/catalog.json')

    def test_catalog_size(self):
        self.assertGreater(self.catalog['stats']['tools'], 1000)

    def test_unique_ids(self):
        ids = [x['id'] for x in self.catalog['tools']]
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_toc_items(self):
        self.assertFalse(any(x['category'] == '📖 Table of Contents' for x in self.catalog['tools']))

    def test_no_space_in_urls(self):
        self.assertFalse(any(' ' in x['url'] for x in self.catalog['tools']))

    def test_chinese_search(self):
        ranked = sorted(((score_tool(x, '域名 DNS 证书历史'), x) for x in self.catalog['tools']), reverse=True, key=lambda v: v[0])
        top_categories = {x['category'] for score, x in ranked[:20] if score > 0}
        self.assertTrue({'Domain and IP Research', 'DNS', 'Web History and Website Capture'} & top_categories)

    def test_restricted_present(self):
        self.assertTrue(any(x['risk_tier'] == 'restricted' for x in self.catalog['tools']))

    def test_biometric_search_is_restricted(self):
        risky = [x for x in self.catalog['tools'] if x['risk_flags']['biometric']]
        self.assertTrue(risky)
        self.assertTrue(any(x['risk_tier'] == 'restricted' for x in risky))


if __name__ == '__main__':
    unittest.main()
