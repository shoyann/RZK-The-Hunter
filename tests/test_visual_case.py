import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "visual_case.py"
FIELDS = [
    "candidate_id",
    "candidate_name",
    "clue_weight",
    "match_score_minus2_to_plus2",
]


class VisualCaseScoringTests(unittest.TestCase):
    def run_score(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "candidates.csv"
            with matrix.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(FIELDS)
                writer.writerows(rows)
            return subprocess.run(
                [sys.executable, str(SCRIPT), "score", str(matrix)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )

    def assert_input_error(self, result, message, row_number=3):
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "", "Invalid input must not produce a ranking")
        self.assertIn(f"Error: row {row_number}:", result.stderr)
        self.assertIn(message, result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_rejects_non_finite_weights_and_scores(self):
        for field_index, field in [(2, FIELDS[2]), (3, FIELDS[3])]:
            for value in ["NaN", "inf", "-inf", "1e309"]:
                with self.subTest(field=field, value=value):
                    invalid = ["A", "Alpha", "1", "1"]
                    invalid[field_index] = value
                    result = self.run_score([["A", "Alpha", "1", "1"], invalid])
                    self.assert_input_error(result, f"{field} must be finite")

    def test_rejects_negative_weight(self):
        result = self.run_score([
            ["A", "Alpha", "1", "1"],
            ["B", "Beta", "-1", "-2"],
        ])
        self.assert_input_error(result, "clue_weight must be non-negative")

    def test_rejects_out_of_range_match_scores(self):
        for value in ["-2.01", "2.01"]:
            with self.subTest(value=value):
                result = self.run_score([["A", "Alpha", "1", value]])
                self.assert_input_error(result, "match score must be between -2 and +2", 2)

    def test_rejects_finite_operands_with_overflowing_product(self):
        for score in ["2", "-2"]:
            with self.subTest(score=score):
                result = self.run_score([["A", "Alpha", "1e308", score]])
                self.assert_input_error(result, "weighted score exceeds the finite numeric range", 2)

    def test_rejects_overflowing_candidate_total(self):
        for score in ["1", "-1"]:
            with self.subTest(score=score):
                result = self.run_score([
                    ["A", "Alpha", "1e308", score],
                    ["A", "Alpha", "1e308", score],
                ])
                self.assert_input_error(result, "candidate total exceeds the finite numeric range")

    def test_valid_scores_preserve_contrary_evidence_and_allow_zero_weight(self):
        result = self.run_score([
            ["A", "Alpha", "3", "2"],
            ["A", "Alpha", "2", "-2"],
            ["A", "Alpha", "2", "-0.5"],
            ["A", "Alpha", "0", "2"],
            ["B", "Beta", "1.5", "1"],
            ["C", "Gamma", "0", "0"],
            ["D", "Delta", "1", "-1"],
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        lines = result.stdout.splitlines()
        self.assertEqual(lines[1:5], [
            "B\tBeta\t1.50\t1\t0\t0",
            "A\tAlpha\t1.00\t2\t2\t1",
            "C\tGamma\t0.00\t0\t0\t0",
            "D\tDelta\t-1.00\t0\t1\t0",
        ])
        self.assertIn("do not override a direct contradiction", result.stdout)


if __name__ == "__main__":
    unittest.main()
