import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPACT_FIELDS = {'id', 'name', 'url', 'risk_tier', 'score'}


class ToolSelectionCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp_dir.cleanup)
        cls.catalog = Path(cls.temp_dir.name) / 'catalog.json'
        cls.empty_catalog = Path(cls.temp_dir.name) / 'empty.json'

        def tool(name, category, risk='low', description='domain registration RDAP WHOIS'):
            slug = name.lower().replace(' ', '-')
            return {
                'id': slug, 'name': name, 'url': f'https://{slug}.example/',
                'domain': f'{slug}.example', 'category': category, 'subcategory': '',
                'description': description, 'tags': ['test'], 'risk_tier': risk,
                'risk_flags': {}, 'risk_reasons': [], 'signals': {}, 'source_line': 1,
            }

        cls.tools = [
            tool('Registrar A', 'Domain and IP Research'),
            tool('Registrar B', 'Domain and IP Research', 'guarded'),
            tool('Registrar C', 'DNS'),
            tool('Registrar D', 'DNS'),
            # Preferred-name bonuses must never bypass risk filtering.
            tool('Icann Lookup', 'Domain and IP Research', 'restricted'),
            tool('Wayback Machine', 'Web History and Website Capture',
                 description='Wayback website archive history capture'),
            tool('Archive Mirror', 'Web History and Website Capture', 'guarded',
                 'website archive history capture'),
            tool('Restricted Archive', 'Web History and Website Capture', 'restricted',
                 'website archive history capture'),
            tool('Company Registry', 'Company Research'),
        ]
        cls.catalog.write_text(json.dumps({'tools': cls.tools}), encoding='utf-8')
        cls.empty_catalog.write_text(json.dumps({'tools': []}), encoding='utf-8')

    def run_cli(self, script, *args, catalog=None):
        return subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / script),
             '--catalog', str(catalog or self.catalog), *args],
            capture_output=True, text=True, encoding='utf-8',
        )

    def run_json(self, script, *args, catalog=None):
        result = self.run_cli(script, *args, '--json', catalog=catalog)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout), result

    def test_search_defaults_to_three_compact_results(self):
        rows, _ = self.run_json('search_catalog.py', 'domain')
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(set(row) == COMPACT_FIELDS for row in rows))
        self.assertTrue(all(row['risk_tier'] != 'restricted' for row in rows))

    def test_search_category_and_risk_filters(self):
        rows, _ = self.run_json('search_catalog.py', 'domain', '--top', '20',
                                '--category', 'DNS', '--max-risk', 'low', '--full')
        self.assertEqual({row['name'] for row in rows}, {'Registrar C', 'Registrar D'})
        self.assertTrue(all(row['category'] == 'DNS' and row['risk_tier'] == 'low' for row in rows))

    def test_search_restricted_requires_explicit_opt_in(self):
        rows, _ = self.run_json('search_catalog.py', 'domain', '--top', '20')
        self.assertNotIn('Icann Lookup', {row['name'] for row in rows})
        for flag in (('--include-restricted',), ('--max-risk', 'restricted')):
            with self.subTest(flag=flag):
                rows, _ = self.run_json('search_catalog.py', 'domain', '--top', '20', *flag)
                self.assertIn('Icann Lookup', {row['name'] for row in rows})

    def test_search_unmatched_json_and_text(self):
        rows, _ = self.run_json('search_catalog.py', 'no-matching-lookup-987654321')
        self.assertEqual(rows, [])
        result = self.run_cli('search_catalog.py', 'no-matching-lookup-987654321')
        self.assertEqual(result.returncode, 1)
        self.assertIn('No matching tools.', result.stdout)

    def test_json_field_selection_and_full_details(self):
        for script, args in (
            ('search_catalog.py', ('domain',)),
            ('select_tools.py', ('--workflow', 'domain', '--stage', 'history')),
        ):
            with self.subTest(script=script):
                output, _ = self.run_json(script, *args, '--fields', 'name,url,description')
                rows = output if script == 'search_catalog.py' else output[0]['tools']
                self.assertTrue(rows)
                self.assertTrue(all(set(row) == {'name', 'url', 'description'} for row in rows))
                output, _ = self.run_json(script, *args, '--full')
                rows = output if script == 'search_catalog.py' else output[0]['tools']
                for row in rows:
                    original = next(tool for tool in self.tools if tool['id'] == row['id'])
                    self.assertEqual({key: value for key, value in row.items() if key != 'score'}, original)
                    self.assertIsInstance(row['score'], (int, float))

    def test_select_defaults_to_first_stage_with_primary_and_backup(self):
        output, result = self.run_json('select_tools.py', '--workflow', 'domain')
        self.assertEqual(len(output), 1)
        self.assertEqual(set(output[0]), {'stage', 'query', 'tools'})
        self.assertEqual(output[0]['stage'], 'Identity and registration')
        self.assertEqual(len(output[0]['tools']), 2)
        self.assertTrue(all(set(row) == COMPACT_FIELDS for row in output[0]['tools']))
        self.assertIn('Selected first stage only:', result.stderr)
        self.assertIn('--all-stages', result.stderr)
        self.assertNotIn('History', result.stdout)

    def test_select_default_text_explains_scope_without_other_stages(self):
        result = self.run_cli('select_tools.py', '--workflow', 'domain')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Selected first stage only:', result.stdout)
        self.assertIn('## Identity and registration', result.stdout)
        self.assertNotIn('## History', result.stdout)
        self.assertNotIn('Wayback Machine', result.stdout)

    def test_select_explicit_stage_slug_and_full_title(self):
        for stage in ('identity-and-registration', 'IDENTITY AND REGISTRATION'):
            with self.subTest(stage=stage):
                output, result = self.run_json('select_tools.py', '--workflow', 'domain', '--stage', stage)
                self.assertEqual([item['stage'] for item in output], ['Identity and registration'])
                self.assertEqual(result.stderr, '')
        output, _ = self.run_json('select_tools.py', '--workflow', 'domain', '--stage', 'history')
        self.assertEqual([item['stage'] for item in output], ['History'])
        self.assertEqual({row['name'] for row in output[0]['tools']}, {'Wayback Machine', 'Archive Mirror'})

    def test_select_all_stages_requires_opt_in_and_keeps_structure(self):
        output, result = self.run_json('select_tools.py', '--workflow', 'domain', '--all-stages', '--full')
        self.assertEqual([item['stage'] for item in output], [
            'Identity and registration', 'DNS and certificates', 'Infrastructure', 'History', 'Reputation',
        ])
        self.assertEqual(result.stderr, '')
        self.assertTrue(all(set(item) == {'stage', 'query', 'tools'} for item in output))
        self.assertTrue(all(row['risk_tier'] != 'restricted' for item in output for row in item['tools']))

    def test_select_low_risk_filter_applies_before_preference_bonus(self):
        output, _ = self.run_json('select_tools.py', '--workflow', 'domain', '--max-risk', 'low',
                                  '--per-stage', '20')
        rows = output[0]['tools']
        self.assertEqual({row['name'] for row in rows}, {'Registrar A', 'Registrar C', 'Registrar D'})
        self.assertTrue(all(row['risk_tier'] == 'low' for row in rows))

    def test_list_stages_does_not_load_catalog(self):
        missing = Path(self.temp_dir.name) / 'missing-catalog.json'
        output, _ = self.run_json('select_tools.py', '--workflow', 'domain', '--list-stages', catalog=missing)
        self.assertEqual(len(output), 5)
        self.assertEqual(output[0]['stage_id'], 'identity-and-registration')
        self.assertTrue(all(set(stage) == {'stage_id', 'stage', 'query'} for stage in output))
        result = self.run_cli('select_tools.py', '--workflow', 'domain', '--list-stages', catalog=missing)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('dns-and-certificates\tDNS and certificates', result.stdout)

    def test_select_empty_stage_reports_no_results(self):
        output, _ = self.run_json('select_tools.py', '--workflow', 'domain', '--stage', 'history',
                                  catalog=self.empty_catalog)
        self.assertEqual(output[0]['tools'], [])
        result = self.run_cli('select_tools.py', '--workflow', 'domain', '--stage', 'history',
                              catalog=self.empty_catalog)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('No suitable catalog match', result.stdout)

    def test_result_limits_must_be_positive_integers(self):
        for script, args, option in (
            ('search_catalog.py', ('domain',), '--top'),
            ('select_tools.py', ('--workflow', 'domain'), '--per-stage'),
        ):
            for value in ('0', '-1', 'nope'):
                with self.subTest(script=script, value=value):
                    result = self.run_cli(script, *args, option, value)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn('must be a positive integer', result.stderr)

    def test_json_options_reject_ambiguous_or_invalid_arguments(self):
        for script, args in (
            ('search_catalog.py', ('domain',)),
            ('select_tools.py', ('--workflow', 'domain')),
        ):
            for options in (
                ('--full',), ('--fields', 'name'),
                ('--json', '--fields', 'nonexistent'), ('--json', '--fields', ''),
                ('--json', '--fields', 'name,'), ('--json', '--fields', 'name', '--full'),
            ):
                with self.subTest(script=script, options=options):
                    result = self.run_cli(script, *args, *options)
                    self.assertEqual(result.returncode, 2, result.stdout)

    def test_invalid_or_conflicting_stages_are_rejected(self):
        for options in (
            ('--stage', 'not-a-stage'), ('--stage', ''), ('--stage', 'history', '--all-stages'),
            ('--list-stages', '--all-stages'), ('--stage', 'history', '--list-stages'),
            ('--list-stages', '--json', '--full'), ('--list-stages', '--json', '--fields', 'name'),
            ('--max-risk', 'restricted'),
        ):
            with self.subTest(options=options):
                result = self.run_cli('select_tools.py', '--workflow', 'domain', *options)
                self.assertEqual(result.returncode, 2, result.stdout)


if __name__ == '__main__':
    unittest.main()
