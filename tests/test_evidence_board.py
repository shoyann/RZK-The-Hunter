import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

try:
    from PIL import Image, ImageFont
except ImportError:
    Image = None

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "evidence_board.py"
MODULE = importlib.util.spec_from_file_location("evidence_board", SCRIPT)
board = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(board)


class EvidenceBoardHelpTests(unittest.TestCase):
    def test_help_without_pillow_and_missing_dependency_guidance(self):
        help_result = subprocess.run([sys.executable, "-S", str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        result = subprocess.run([sys.executable, "-S", str(SCRIPT), "case.json", "--out", "board.png"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("uv run", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


@unittest.skipIf(Image is None, "Optional Pillow dependency is not installed")
class EvidenceBoardTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.spec = self.root / "input.json"
        self.output = self.root / "result.png"
        self.subject = self.root / "subject.jpg"
        # EXIF orientation 6 rotates the landscape file into a portrait display.
        image = Image.new("RGB", (240, 120), "red")
        exif = Image.Exif()
        exif[274] = 6
        image.save(self.subject, exif=exif)
        Image.new("RGBA", (90, 60), (0, 0, 255, 128)).save(self.root / "reference.png")
        self.data = {
            "schema_version": 1,
            "subject": {"image": "subject.jpg", "caption": "Original photo", "source": "Supplied by user"},
            "references": [{"image": "reference.png", "caption": "Comparison photo", "source": "https://example.org/reference"}],
            "matches": ["Curved facade and windows"],
            "uncertainties": ["Reference has a different viewpoint"],
        }

    def write_spec(self):
        self.spec.write_text(json.dumps(self.data), encoding="utf-8")

    def run_board(self, **options):
        self.write_spec()
        return board.render(self.spec, self.output, **options)

    def test_relative_assets_provenance_exif_and_originals_preserved(self):
        self.write_spec()
        originals = {path: path.read_bytes() for path in (self.spec, self.subject, self.root / "reference.png")}
        result = board.render(self.spec, self.output)
        self.assertTrue(self.output.is_file())
        saved = json.loads(self.output.with_suffix(".json").read_text())
        self.assertEqual(result, saved)
        self.assertEqual(saved["board_sha256"], hashlib.sha256(self.output.read_bytes()).hexdigest())
        self.assertEqual(saved["spec_sha256"], hashlib.sha256(originals[self.spec]).hexdigest())
        self.assertEqual(saved["claims"]["camera"]["status"], "unverified")
        self.assertEqual(saved["claims"]["matches"][0]["status"], "analyst_assertion")
        subject = saved["assets"][0]
        self.assertEqual(subject["sha256"], hashlib.sha256(originals[self.subject]).hexdigest())
        self.assertEqual(subject["original_size"], [240, 120])
        self.assertEqual(subject["transformations"]["display_size"], [450, 900])
        self.assertFalse(subject["transformations"]["cropped"])
        self.assertFalse(subject["transformations"]["stretched"])
        self.assertEqual(saved["assets"][1]["source"], "https://example.org/reference")
        for path, content in originals.items():
            self.assertEqual(path.read_bytes(), content)

    def test_invalid_schema_and_claims_fail_before_writing(self):
        mutations = [
            ("schema_version", True), ("schema_version", 2), ("title", 123),
            ("references", []), ("references", "invalid"), ("matches", [3]),
            ("uncertainties", ["x"] * 13), ("camera", {"status": "verified"}),
            ("camera", {"status": "unknown"}), ("camera", {"status": "verified", "evidence": " "}),
        ]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                old = self.data.get(key)
                self.data[key] = value
                with self.assertRaises(ValueError):
                    self.run_board()
                if old is None:
                    self.data.pop(key)
                else:
                    self.data[key] = old
                self.assertFalse(self.output.exists())

    def test_verified_camera_requires_evidence_and_retains_assertion_status(self):
        self.data["camera"] = {"status": "verified", "evidence": "Analyst checked documented camera geometry, case item 12"}
        record = self.run_board()
        camera = record["claims"]["camera"]
        self.assertEqual(camera["status"], "verified")
        self.assertIn("not_independently_validated", camera["validation"])
        self.assertEqual(camera["evidence"], self.data["camera"]["evidence"])

    def test_local_files_and_reference_attribution_required(self):
        reference = self.data["references"][0]
        for key, value in (("source", " "), ("image", "https://example.org/a.jpg"), ("image", "missing.jpg")):
            with self.subTest(key=key):
                old = reference[key]
                reference[key] = value
                with self.assertRaises((ValueError, FileNotFoundError)):
                    self.run_board()
                reference[key] = old
                self.assertFalse(self.output.exists())

    def test_input_and_sidecar_collisions_never_overwritten_even_with_force(self):
        self.write_spec()
        for output in (self.root / "reference.png", self.spec.with_suffix(".png")):
            before = {path: path.read_bytes() for path in self.root.iterdir()}
            with self.assertRaisesRegex(ValueError, "overwrite an input"):
                board.render(self.spec, output, force=True)
            self.assertEqual(before, {path: path.read_bytes() for path in self.root.iterdir()})

    def test_existing_outputs_need_explicit_force(self):
        self.run_board()
        before = self.output.read_bytes()
        with self.assertRaisesRegex(ValueError, "already exists"):
            board.render(self.spec, self.output)
        self.assertEqual(before, self.output.read_bytes())
        self.data["title"] = "A revised board"
        self.run_board(force=True)
        self.assertNotEqual(before, self.output.read_bytes())

    def test_directory_sidecar_does_not_replace_existing_image(self):
        self.output.write_bytes(b"existing image")
        self.output.with_suffix(".json").mkdir()
        with self.assertRaisesRegex(ValueError, "not a regular file"):
            self.run_board(force=True)
        self.assertEqual(self.output.read_bytes(), b"existing image")

    def test_failed_second_publish_restores_existing_pair(self):
        self.run_board()
        sidecar = self.output.with_suffix(".json")
        before = [path.read_bytes() for path in (self.output, sidecar)]
        self.data["title"] = "Replacement that must roll back"
        real_replace = board.os.replace
        calls = []

        def fail_second(source, destination):
            calls.append(destination)
            if len(calls) == 2:
                raise OSError("Simulated second publication failure")
            return real_replace(source, destination)

        with patch.object(board.os, "replace", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "Simulated"):
                self.run_board(force=True)
        self.assertEqual(before, [path.read_bytes() for path in (self.output, sidecar)])

    def test_three_references_put_notes_beside_last_panel(self):
        self.data["references"] *= 3
        result = self.run_board()
        matches_heading = result["text_boxes"][-5]
        third_reference = result["assets"][3]["display_box"]
        self.assertGreater(matches_heading["x"], third_reference[2])
        self.assertLess(matches_heading["y"], third_reference[3])

    def test_long_sources_wrap_without_clipping_and_text_bounds_fit(self):
        self.data["references"] *= 4
        for item in self.data["references"]:
            item["source"] = "https://example.org/" + "resource" * 50
        result = self.run_board()
        width, height = result["board_size"]
        for block in result["text_boxes"]:
            self.assertLessEqual(block["x"] + block["width"], width)
            self.assertLessEqual(block["y"] + block["height"], height)
        font = ImageFont.truetype(result["font"], 20)
        for line in board.wrapped(self.data["references"][0]["source"], font, 475):
            self.assertLessEqual(font.getlength(line), 475)

    def test_oversized_layout_is_rejected_instead_of_truncating(self):
        self.data["matches"] = ["M" * 500] * 12
        self.data["uncertainties"] = ["M" * 500] * 12
        with self.assertRaisesRegex(ValueError, "6400 pixels"):
            self.run_board()
        self.assertFalse(self.output.exists())

    def test_unavailable_explicit_font_is_actionable(self):
        with self.assertRaisesRegex(ValueError, "--font"):
            self.run_board(font_path=self.root / "missing.ttf")
        self.assertFalse(self.output.exists())

    def test_word_wrapping_preserves_words_when_they_fit(self):
        result = self.run_board()
        font = ImageFont.truetype(result["font"], 20)
        width = font.getlength("One short phrase")
        lines = board.wrapped("One short phrase another short phrase", font, width)
        self.assertEqual(" ".join(lines), "One short phrase another short phrase")
        self.assertEqual(lines[0], "One short phrase")

    def test_cjk_bullet_wraps_without_isolated_prefix_or_blank_lines(self):
        class FixedWidthCjkFont:
            def getlength(self, text):
                return sum(20 if board.unicodedata.east_asian_width(c) in ("W", "F") else 10 for c in text)

        text = "- 识别建筑不等于确定拍摄站位；未计算朝向或误差半径。"
        font = FixedWidthCjkFont()
        lines = board.wrapped(text, font, 476)
        self.assertEqual(len(lines), 2)
        self.assertEqual("".join(lines), text)
        for line in lines:
            self.assertNotIn(line.strip(), ("", "-", "。"))
            self.assertLessEqual(font.getlength(line), 476)

    def test_long_cjk_run_after_prefix_never_overflows_actual_font(self):
        result = self.run_board()
        font = ImageFont.truetype(result["font"], 20)
        for prefix in ("-", "I"):
            text = prefix + " " + "中" * 50
            lines = board.wrapped(text, font, 475)
            self.assertEqual("".join(lines), text)
            for line in lines:
                self.assertNotIn(line.strip(), ("", prefix))
                self.assertLessEqual(font.getlength(line), 475)

    def test_cjk_glyphs_supported_or_fail_actionably(self):
        self.data["title"] = "建筑证据对照"
        self.data["matches"] = ["圆弧外墙与横向窗带吻合"]
        try:
            result = self.run_board()
        except ValueError as exc:
            self.assertIn("--font", str(exc))
        else:
            self.assertEqual(result["title"], self.data["title"])


if __name__ == "__main__":
    unittest.main()
