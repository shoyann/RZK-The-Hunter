import json
import subprocess
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

    def test_unmatched_query_has_no_catalog_matches(self):
        query = 'zzzzunmatchedreviewterm987654321'
        self.assertTrue(all(score_tool(tool, query) == 0 for tool in self.catalog['tools']))

    def test_matched_tools_keep_low_risk_preference(self):
        tool = {'name': 'Domain registry', 'risk_tier': 'guarded'}
        for query in ('registry', '域名'):
            with self.subTest(query=query):
                guarded_score = score_tool(tool, query)
                low_score = score_tool({**tool, 'risk_tier': 'low'}, query)
                self.assertGreater(guarded_score, 0)
                self.assertAlmostEqual(low_score, guarded_score + 0.4)

    def test_cli_unmatched_text_reports_no_results(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/search_catalog.py'),
             'zzzzunmatchedreviewterm987654321'],
            capture_output=True, text=True, encoding='utf-8',
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('No matching tools.', result.stdout)

    def test_cli_unmatched_json_returns_empty_list(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/search_catalog.py'),
             'zzzzunmatchedreviewterm987654321', '--json'],
            capture_output=True, text=True, encoding='utf-8',
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])

    def test_restricted_present(self):
        self.assertTrue(any(x['risk_tier'] == 'restricted' for x in self.catalog['tools']))

    def test_biometric_search_is_restricted(self):
        risky = [x for x in self.catalog['tools'] if x['risk_flags']['biometric']]
        self.assertTrue(risky)
        self.assertTrue(any(x['risk_tier'] == 'restricted' for x in risky))


if __name__ == '__main__':
    unittest.main()
