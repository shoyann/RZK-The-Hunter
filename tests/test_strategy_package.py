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


if __name__ == "__main__":
    unittest.main()
