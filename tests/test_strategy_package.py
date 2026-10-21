import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import verify_package


class StrategyPackageTests(unittest.TestCase):
    def test_live_versions_and_package(self):
        errors = []
        verify_package.verify_versions(errors)
        verify_package.verify_strategy_package(errors)
        verify_package.verify_execution_package(errors)
        verify_package.verify_evidence_board_package(errors)
        self.assertEqual(errors, [])

    def test_manifest_omission_is_caught(self):
        with tempfile.TemporaryDirectory() as folder:
            staging = Path(folder)
            entries = (ROOT / "manifest.txt").read_text().splitlines()
            for rel in entries:
                dest = staging / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, dest)
            missing = "references/adaptive-investigation-strategy.md"
            (staging / "manifest.txt").write_text("\n".join(x for x in entries if x != missing))
            errors = []
            with patch.object(verify_package, "ROOT", staging):
                verify_package.verify_strategy_package(errors)
            self.assertTrue(any(missing in error for error in errors))

    def test_execution_resources_must_be_packaged(self):
        with tempfile.TemporaryDirectory() as folder:
            staging = Path(folder)
            entries = (ROOT / 'manifest.txt').read_text().splitlines()
            for rel in entries:
                destination = staging / rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, destination)
            for missing in ('references/execution-modes.md', 'tests/test_evidence_ledger.py'):
                with self.subTest(missing=missing):
                    (staging / 'manifest.txt').write_text('\n'.join(x for x in entries if x != missing))
                    errors = []
                    with patch.object(verify_package, 'ROOT', staging):
                        verify_package.verify_execution_package(errors)
                    self.assertTrue(any(missing in error for error in errors))

    def test_evidence_board_resources_must_be_packaged(self):
        with tempfile.TemporaryDirectory() as folder:
            staging = Path(folder)
            entries = (ROOT / 'manifest.txt').read_text().splitlines()
            for rel in entries:
                destination = staging / rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, destination)
            for missing in ('references/visual-evidence-board.md', 'scripts/evidence_board.py', 'tests/test_evidence_board.py'):
                with self.subTest(missing=missing):
                    (staging / 'manifest.txt').write_text('\n'.join(x for x in entries if x != missing))
                    errors = []
                    with patch.object(verify_package, 'ROOT', staging):
                        verify_package.verify_evidence_board_package(errors)
                    self.assertTrue(any(missing in error for error in errors))


if __name__ == "__main__":
    unittest.main()
