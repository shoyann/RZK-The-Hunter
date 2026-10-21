#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10.4"]
# ///
"""Render a local evidence board; assertions remain the analyst's responsibility."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone


def nonempty(value, name, limit=1000):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{name} must be nonempty text of at most {limit} characters")
    if any(ord(c) < 32 and c not in "\n\t" for c in value):
        raise ValueError(f"{name} contains unsupported control characters")
    return value.strip()


def keys(value, allowed, name):
    if not isinstance(value, dict) or set(value) - set(allowed):
        raise ValueError(f"{name} must be an object with only: {', '.join(allowed)}")


def load_spec(path):
    if path.stat().st_size > 100_000:
        raise ValueError("Spec exceeds 100 KB")
    spec = json.loads(path.read_text(encoding="utf-8"))
    keys(spec, ("schema_version", "title", "subject", "references", "matches", "uncertainties", "camera"), "spec")
    if type(spec.get("schema_version")) is not int or spec["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    spec["title"] = nonempty(spec.get("title", "Visual evidence board"), "title", 180)
    refs = spec.get("references")
    if not isinstance(refs, list) or not 1 <= len(refs) <= 4:
        raise ValueError("references must contain 1 to 4 images")
    for index, asset in enumerate([spec.get("subject")] + refs):
        name = "subject" if index == 0 else f"references[{index - 1}]"
        keys(asset, ("image", "caption", "source"), name)
        for field, limit in (("image", 4096), ("caption", 300), ("source", 1000)):
            asset[field] = nonempty(asset.get(field), f"{name}.{field}", limit)
        if "://" in asset["image"] or asset["image"].startswith("data:"):
            raise ValueError(f"{name}.image must be a local file; no network downloads")
        asset["path"] = (path.parent / asset["image"]).resolve(strict=True)
        if not asset["path"].is_file():
            raise ValueError(f"{name}.image must be a local file")
    for field in ("matches", "uncertainties"):
        items = spec.setdefault(field, [])
        if not isinstance(items, list) or len(items) > 12:
            raise ValueError(f"{field} must be a list of at most 12 strings")
        spec[field] = [nonempty(item, field, 500) for item in items]
    camera = spec.setdefault("camera", {"status": "unverified"})
    keys(camera, ("status", "evidence"), "camera")
    if camera.get("status") not in ("unverified", "verified"):
        raise ValueError("camera.status must be unverified or verified")
    if camera["status"] == "verified" or "evidence" in camera:
        camera["evidence"] = nonempty(camera.get("evidence"), "camera.evidence", 1000)
    return spec


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_outputs(outputs, inputs, force):
    for output in outputs:
        if output.exists() and not output.is_file():
            raise ValueError(f"Output is not a regular file: {output}")
        if any(output.resolve() == item.resolve() or
               (output.exists() and os.path.samefile(output, item)) for item in inputs):
            raise ValueError(f"Output would overwrite an input: {output}")
        if output.exists() and not force:
            raise ValueError(f"Output already exists: {output}; choose another name or use --force")


def choose_font(ImageFont, requested, text):
    candidates = [requested] if requested else [
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/mnt/c/Windows/Fonts/msyh.ttc"),
        Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts/msyh.ttc",
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts/arial.ttf",
    ]
    characters = set(text) - set(" \t\r\n")
    for candidate in candidates:
        if candidate and candidate.is_file():
            try:
                font = ImageFont.truetype(str(candidate), 22)
                missing = font.getmask(chr(0x10FFFF))
                signature = (missing.size, bytes(missing))
                if all((mask.size, bytes(mask)) != signature
                       for mask in (font.getmask(c) for c in characters)):
                    return candidate
            except OSError:
                pass
    raise ValueError("No font covers the supplied text. Install a suitable font (e.g. Noto Sans CJK) or pass --font /path/to/font.ttf")


def wrapped(text, font, width):
    """Keep Latin words together; wrap CJK characters and long URLs safely."""
    lines = []
    for paragraph in text.expandtabs(4).split("\n"):
        tokens, word = [], ""
        for char in paragraph:
            if char.isspace() or unicodedata.east_asian_width(char) in ("W", "F"):
                if word:
                    tokens.append(word)
                    word = ""
                tokens.append(char)
            else:
                word += char
        if word:
            tokens.append(word)
        line, start = "", len(lines)
        for token in tokens:
            if line and font.getlength(token) <= width and font.getlength(line + token) > width:
                lines.append(line.rstrip())
                line = ""
            for char in token:
                if font.getlength(char) > width:
                    raise ValueError("A text glyph exceeds the available panel width")
                if line and font.getlength(line + char) > width:
                    lines.append(line.rstrip())
                    line = ""
                if not line and char.isspace():
                    continue
                line += char
        if line or len(lines) == start:
            lines.append(line.rstrip())
    return lines


def render(spec_path, out, font_path=None, force=False):
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:
        raise ValueError("Pillow is required. Run: uv run scripts/evidence_board.py SPEC --out board.png (or install Pillow>=10.4)") from exc
    spec_path, out = spec_path.resolve(), out.resolve()
    if out.suffix.lower() != ".png":
        raise ValueError("--out must have a .png extension")
    spec = load_spec(spec_path)
    assets = [spec["subject"]] + spec["references"]
    sidecar = out.with_suffix(".json")
    check_outputs((out, sidecar), [spec_path] + [a["path"] for a in assets], force)
    camera = spec["camera"]
    camera_label = ("Camera position: NOT VERIFIED" if camera["status"] == "unverified"
                    else "Camera position: VERIFIED (analyst assertion)")
    strings = [spec["title"], camera_label, "Source: ABCDE References Matches (analyst assertions) Uncertainties",
               "No matches supplied. No additional limitations supplied. Presentation only; claims are not independently validated."]
    strings += [a[k] for a in assets for k in ("caption", "source")]
    strings += spec["matches"] + spec["uncertainties"] + [camera.get("evidence", "")]
    selected_font = choose_font(ImageFont, font_path, " ".join(strings))
    check_outputs((out, sidecar), [spec_path, selected_font] + [a["path"] for a in assets], force)
    fonts = {size: ImageFont.truetype(str(selected_font), size) for size in (20, 24, 32)}
    blocks = []

    def text_block(text, x, y, width, size=24, color="#18232b"):
        font = fonts[size]
        lines = wrapped(text, font, width)
        ascent, descent = font.getmetrics()
        step = ascent + descent + 6
        blocks.append({"lines": lines, "x": x, "y": y, "width": width,
                       "height": len(lines) * step, "size": size, "color": color, "step": step})
        return y + len(lines) * step

    width, margin, gap = 1600, 32, 28
    left_width, right_x = 530, 590
    right_width = width - margin - right_x
    y0 = text_block(spec["title"], margin, margin, width - 2 * margin, 32) + 16
    y0 = text_block(camera_label, margin, y0, width - 2 * margin, 24, "#9d3617") + 22
    if camera.get("evidence"):
        y0 = text_block("Camera evidence: " + camera["evidence"], margin, y0, width - 2 * margin, 20) + 18
    panels = []

    def panel(asset, index, x, y, panel_width, image_height):
        heading_end = text_block(f"{chr(65 + index)}: {asset['caption']}", x, y, panel_width)
        box = (x, heading_end + 8, x + panel_width, heading_end + 8 + image_height)
        panels.append((asset, box))
        return text_block("Source: " + asset["source"], x, box[3] + 10, panel_width, 20) + 22

    left_end = panel(assets[0], 0, margin, y0, left_width, 900)
    y = y0
    refs = assets[1:]
    cols = 1 if len(refs) == 1 else 2
    cell_width = (right_width - gap * (cols - 1)) // cols
    notes_x, notes_width, notes_start = right_x, right_width, None
    for row in range(0, len(refs), cols):
        if len(refs) == 3 and row == 2:
            notes_x, notes_width, notes_start = right_x + cell_width + gap, cell_width, y
        ends = [panel(asset, row + col + 1, right_x + col * (cell_width + gap),
                      y, cell_width, 440 if cols == 1 else 340)
                for col, asset in enumerate(refs[row:row + cols])]
        y = max(ends) + 12
    grid_end = y
    if notes_start is not None:
        y = notes_start
    for heading, items, empty in (("Matches (analyst assertions)", spec["matches"], "No matches supplied."),
                                 ("Uncertainties", spec["uncertainties"], "No additional limitations supplied.")):
        y = text_block(heading, notes_x, y + 12, notes_width) + 6
        for line in items or [empty]:
            y = text_block("- " + line, notes_x, y, notes_width, 20) + 5
    footer_y = max(y, left_end, grid_end) + 12
    height = text_block("Presentation only; claims are not independently validated.", margin,
                        footer_y, width - 2 * margin, 20, "#465962") + margin
    if height > 6400:
        raise ValueError("Text creates a board over 6400 pixels tall; shorten captions, source labels or claims")
    canvas = Image.new("RGB", (width, height), "#f2f4f5")
    draw = ImageDraw.Draw(canvas)
    provenance = []
    for asset, box in panels:
        try:
            original = Image.open(asset["path"])
        except Image.DecompressionBombError as exc:
            raise ValueError("Image exceeds Pillow's safe pixel limit; supply a documented smaller derivative") from exc
        with original:
            if original.width * original.height > 50_000_000 or max(original.size) > 20000:
                raise ValueError("Input images must be at most 50 megapixels and 20000 pixels per side")
            if getattr(original, "n_frames", 1) > 1:
                raise ValueError("Animated/multi-frame images are unsupported; supply an explicit frame")
            original_size = list(original.size)
            orientation = original.getexif().get(274, 1)
            upright = ImageOps.exif_transpose(original).convert("RGBA")
            display = ImageOps.contain(upright, (box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
        x, y = box[0] + (box[2] - box[0] - display.width) // 2, box[1] + (box[3] - box[1] - display.height) // 2
        draw.rectangle(box, fill="#e2e7ea")
        canvas.paste(display, (x, y), display)
        provenance.append({"image": asset["image"], "caption": asset["caption"], "source": asset["source"],
                           "sha256": sha256(asset["path"]), "original_size": original_size,
                           "display_box": [x, y, x + display.width, y + display.height],
                           "transformations": {"fit": "contain", "cropped": False, "stretched": False,
                                               "exif_orientation": orientation, "exif_transpose": True,
                                               "display_size": list(display.size), "alpha_background": "#e2e7ea"}})
    for block in blocks:
        for index, line in enumerate(block["lines"]):
            draw.text((block["x"], block["y"] + index * block["step"]), line,
                      font=fonts[block["size"]], fill=block["color"], anchor="lt")
    record = {"schema_version": 1, "created_utc": datetime.now(timezone.utc).isoformat(),
              "title": spec["title"], "spec_sha256": sha256(spec_path), "board_size": [width, height],
              "font": str(selected_font), "assets": provenance,
              "claims": {"matches": [{"text": item, "status": "analyst_assertion"} for item in spec["matches"]],
                         "uncertainties": spec["uncertainties"],
                         "camera": {**camera, "validation": "not_independently_validated_by_renderer"}},
              "text_boxes": [{"x": b["x"], "y": b["y"], "width": b["width"], "height": b["height"]} for b in blocks]}
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = []
    try:
        for destination in (out, sidecar):
            fd, name = tempfile.mkstemp(prefix=".evidence-board-", dir=destination.parent)
            os.close(fd)
            temporary.append(Path(name))
        canvas.save(temporary[0], format="PNG")
        record["board_sha256"] = sha256(temporary[0])
        temporary[1].write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # Keep the previous pair recoverable if publishing the second file fails.
        with tempfile.TemporaryDirectory(prefix=".evidence-backup-", dir=out.parent) as backup_dir:
            backups, published = {}, []
            for index, destination in enumerate((out, sidecar)):
                if destination.exists():
                    backup = Path(backup_dir) / str(index)
                    shutil.copy2(destination, backup)
                    backups[destination] = backup
            try:
                for temporary_path, destination in zip(temporary, (out, sidecar)):
                    os.replace(temporary_path, destination)
                    published.append(destination)
            except OSError:
                for destination in reversed(published):
                    if destination in backups:
                        os.replace(backups[destination], destination)
                    else:
                        destination.unlink(missing_ok=True)
                raise
    finally:
        for temporary_path in temporary:
            temporary_path.unlink(missing_ok=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="UTF-8 JSON spec; image paths are relative to this file")
    parser.add_argument("--out", type=Path, required=True, help="PNG destination; a JSON provenance sidecar is also written")
    parser.add_argument("--font", type=Path, help="Local TTF/OTF/TTC font covering all supplied text")
    parser.add_argument("--force", action="store_true", help="Replace existing outputs, never input files")
    args = parser.parse_args()
    try:
        render(args.spec, args.out, args.font, args.force)
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(f"Wrote {args.out} and {args.out.with_suffix('.json')}")


if __name__ == "__main__":
    main()
