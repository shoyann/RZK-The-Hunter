import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'evidence_ledger.py'
sys.path.insert(0, str(ROOT / 'scripts'))
import evidence_ledger


class EvidenceLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.ledger = self.directory / 'case' / 'evidence.csv'

    def run_cli(self, *args, input_text=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            input=input_text, capture_output=True, text=True, encoding='utf-8',
            timeout=10,
        )

    def batch(self, *rows):
        return self.run_cli('add-batch', self.ledger, '--input', '-',
                            input_text='\n'.join(json.dumps(row) for row in rows))

    def read_rows(self):
        with self.ledger.open(encoding='utf-8', newline='') as handle:
            return list(csv.DictReader(handle))

    def test_batch_file_auto_initializes_and_preserves_ids_and_defaults(self):
        packet = self.directory / 'findings.jsonl'
        packet.write_text('\n'.join(json.dumps(row) for row in [
            {'finding_id': 'E-001', 'claim': 'First observation'},
            {'finding_id': '证据-2', 'claim': 'Comma, quote " and\nnewline',
             'confidence': 'high', 'notes': 'Analyst note', 'source_type': 'primary'},
        ]), encoding='utf-8')
        result = self.run_cli('add-batch', self.ledger, '--input', packet)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), 'Added 2 findings.')
        rows = self.read_rows()
        self.assertEqual([row['finding_id'] for row in rows], ['E-001', '证据-2'])
        self.assertEqual(rows[0]['confidence'], 'low')
        self.assertEqual(rows[0]['label'], 'single-source lead')
        self.assertTrue(rows[0]['accessed_at'])
        self.assertEqual(rows[1]['claim'], 'Comma, quote " and\nnewline')
        self.assertEqual(rows[1]['analyst_notes'], 'Analyst note')

    def test_stdin_appends_after_single_add_and_hashes_files(self):
        result = self.run_cli('add', self.ledger, '--claim', 'Existing', '--finding-id', 'A')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        artifact = self.directory / 'source.txt'
        artifact.write_bytes(b'original artifact')
        result = self.batch({'finding_id': 'B', 'claim': 'New', 'file': str(artifact),
                             'accessed_at': '2026-10-16T01:00:00+00:00'})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        rows = self.read_rows()
        self.assertEqual([row['finding_id'] for row in rows], ['A', 'B'])
        self.assertEqual(rows[1]['file_sha256'], hashlib.sha256(artifact.read_bytes()).hexdigest())
        self.assertEqual(rows[1]['accessed_at'], '2026-10-16T01:00:00+00:00')

    def test_invalid_batch_leaves_existing_ledger_byte_for_byte_unchanged(self):
        self.assertEqual(self.run_cli('add', self.ledger, '--claim', 'Existing').returncode, 0)
        before = self.ledger.read_bytes()
        invalid_rows = [
            {}, [], {'claim': 'Bad', 'confidence': 'certain'},
            {'claim': 'Bad', 'source_type': 'invented'},
            {'claim': 'Bad', 'notes': 42}, {'claim': 'Bad', 'unknown': 'value'},
            {'claim': 'Bad', 'file': str(self.directory / 'missing')},
        ]
        for row in invalid_rows:
            with self.subTest(row=row):
                result = self.batch({'finding_id': 'NEW', 'claim': 'Valid first row'}, row)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('line 2:', result.stdout)
                self.assertEqual(self.ledger.read_bytes(), before)
        result = self.run_cli('add-batch', self.ledger, '--input', '-',
                              input_text='{"claim": "Valid"}\n{malformed json}\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.ledger.read_bytes(), before)

    def test_invalid_batch_does_not_create_ledger_or_directory(self):
        result = self.batch({'claim': 'Valid'}, {'claim': 'Bad', 'confidence': 'certain'})
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.ledger.parent.exists())

    def test_empty_batch_is_a_noop_and_blank_lines_are_allowed(self):
        result = self.run_cli('add-batch', self.ledger, '--input', '-', input_text='\n \n')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout.strip(), 'Added 0 findings.')
        self.assertFalse(self.ledger.exists())
        result = self.run_cli('add-batch', self.ledger, '--input', '-',
                              input_text='\n{"claim": "One"}\n\n{"claim": "Two"}\n')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(len(self.read_rows()), 2)

    def test_invalid_existing_header_is_not_overwritten(self):
        self.ledger.parent.mkdir()
        self.ledger.write_text('unrelated,columns\nkeep,this\n', encoding='utf-8')
        before = self.ledger.read_bytes()
        result = self.batch({'claim': 'Valid'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unexpected CSV header', result.stdout)
        self.assertEqual(self.ledger.read_bytes(), before)

    def test_failed_commit_keeps_original_and_removes_temporary_file(self):
        evidence_ledger.init(self.ledger, False)
        before = self.ledger.read_bytes()
        rows = [evidence_ledger.prepare_row({'claim': 'New'})]
        with patch.object(evidence_ledger.os, 'replace', side_effect=OSError('write failed')):
            with self.assertRaisesRegex(OSError, 'write failed'):
                evidence_ledger.append_batch(self.ledger, rows)
        self.assertEqual(self.ledger.read_bytes(), before)
        self.assertEqual(list(self.ledger.parent.iterdir()), [self.ledger])

    def test_init_and_single_add_remain_available(self):
        self.assertEqual(self.run_cli('init', self.ledger).returncode, 0)
        self.assertNotEqual(self.run_cli('init', self.ledger).returncode, 0)
        result = self.run_cli('add', self.ledger, '--claim', 'Single', '--notes', 'Note')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.read_rows()[0]['analyst_notes'], 'Note')
        self.assertEqual(self.run_cli('init', self.ledger, '--force').returncode, 0)
        self.assertEqual(self.read_rows(), [])

    def assert_writers_reject_locked_ledger(self, ledger):
        commands = [
            ('init', ledger, '--force'),
            ('add', ledger, '--claim', 'Concurrent single finding'),
            ('add-batch', ledger, '--input', '-'),
        ]
        for command in commands:
            with self.subTest(command=command[0], path=str(ledger)):
                result = self.run_cli(*command, input_text='{"claim": "Concurrent batch finding"}\n')
                self.assertEqual(result.returncode, 1)
                self.assertIn('Ledger is locked:', result.stdout)
                self.assertIn('only after confirming no writer is active', result.stdout)

    def test_concurrent_init_add_and_batch_fail_without_touching_existing_ledger(self):
        self.assertEqual(self.batch({'finding_id': 'ORIGINAL', 'claim': 'Keep evidence'}).returncode, 0)
        before = self.ledger.read_bytes()
        lock = self.ledger.with_name(f'{self.ledger.name}.lock')
        with evidence_ledger.ledger_lock(self.ledger):
            owner = lock.read_bytes()
            self.assert_writers_reject_locked_ledger(self.ledger)
            self.assertEqual(self.ledger.read_bytes(), before)
            self.assertEqual(lock.read_bytes(), owner, 'Contending writers must not remove the owner lock')
        self.assertFalse(lock.exists())
        self.assertEqual(self.batch({'finding_id': 'NEXT', 'claim': 'After lock release'}).returncode, 0)
        self.assertEqual([row['finding_id'] for row in self.read_rows()], ['ORIGINAL', 'NEXT'])

    def test_concurrent_writers_cannot_initialize_missing_ledger(self):
        with evidence_ledger.ledger_lock(self.ledger):
            self.assert_writers_reject_locked_ledger(self.ledger)
            self.assertFalse(self.ledger.exists())
        self.assertEqual(list(self.ledger.parent.iterdir()), [])

    def test_path_aliases_share_the_same_lock(self):
        evidence_ledger.init(self.ledger, False)
        alias_directory = self.directory / 'alias'
        try:
            alias_directory.symlink_to(self.ledger.parent, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'directory symlinks unavailable: {exc}')
        alias = alias_directory / self.ledger.name
        with evidence_ledger.ledger_lock(self.ledger):
            self.assert_writers_reject_locked_ledger(alias)
        self.assertEqual(self.batch({'claim': 'Original'}).returncode, 0)
        result = self.run_cli('add-batch', alias, '--input', '-', input_text='{"claim": "Via alias"}\n')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([row['claim'] for row in self.read_rows()], ['Original', 'Via alias'])

    def test_stale_lock_is_never_automatically_removed(self):
        self.ledger.parent.mkdir()
        lock = self.ledger.with_name(f'{self.ledger.name}.lock')
        lock.write_text('stale owner record\n', encoding='ascii')
        self.assert_writers_reject_locked_ledger(self.ledger)
        self.assertEqual(lock.read_text(), 'stale owner record\n')
        self.assertFalse(self.ledger.exists())

    def test_release_does_not_remove_replacement_lock(self):
        lock = self.ledger.with_name(f'{self.ledger.name}.lock')
        with evidence_ledger.ledger_lock(self.ledger):
            lock.unlink()
            lock.write_text('different owner\n', encoding='ascii')
        self.assertEqual(lock.read_text(), 'different owner\n')


if __name__ == '__main__':
    unittest.main()
