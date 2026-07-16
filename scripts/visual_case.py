#!/usr/bin/env python3
"""Initialize and score a multi-signal image/video geolocation case."""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

FILES = {
    "visual-clues.csv": TEMPLATES / "visual-clue-inventory.csv",
    "location-candidates.csv": TEMPLATES / "location-candidate-matrix.csv",
    "image-geolocation-report.md": TEMPLATES / "image-geolocation-report.md",
}


def init_case(case_dir: Path, force: bool = False) -> int:
    case_dir.mkdir(parents=True, exist_ok=True)
    created = []
    skipped = []
    for output_name, template in FILES.items():
        destination = case_dir / output_name
        if destination.exists() and not force:
            skipped.append(output_name)
            continue
        shutil.copyfile(template, destination)
        created.append(output_name)

    checklist = case_dir / "workflow-checklist.md"
    if not checklist.exists() or force:
        checklist.write_text(
            """# Visual Investigation Checklist

- [ ] Exact target and viewpoint relationship defined
- [ ] Original file preserved and hashed
- [ ] Full-frame scene model written before searching
- [ ] Grid and semantic crop sweep completed
- [ ] Alternate text/OCR readings recorded
- [ ] At least three clue families inventoried
- [ ] At least two candidate locations kept alive
- [ ] Source lineages recorded
- [ ] Exact-object near-match test completed
- [ ] Camera/object/road geometry verified
- [ ] Two deliberate falsification tests completed
- [ ] Contradictions and unresolved questions reported
""",
            encoding="utf-8",
        )
        created.append("workflow-checklist.md")
    else:
        skipped.append("workflow-checklist.md")

    print(f"Case directory: {case_dir}")
    if created:
        print("Created:", ", ".join(created))
    if skipped:
        print("Skipped existing files:", ", ".join(skipped))
    return 0


def parse_float(value: str, field: str, row_number: int) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"row {row_number}: invalid {field}={value!r}") from exc


def score_candidates(matrix_path: Path) -> int:
    if not matrix_path.exists():
        print(f"Matrix not found: {matrix_path}", file=sys.stderr)
        return 2

    totals: dict[str, float] = defaultdict(float)
    names: dict[str, str] = {}
    positive: dict[str, int] = defaultdict(int)
    negative: dict[str, int] = defaultdict(int)
    contradictions: dict[str, int] = defaultdict(int)

    with matrix_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {
            "candidate_id",
            "candidate_name",
            "clue_weight",
            "match_score_minus2_to_plus2",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            print(f"Missing columns: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2

        for row_number, row in enumerate(reader, start=2):
            candidate_id = (row.get("candidate_id") or "").strip()
            if not candidate_id:
                continue
            candidate_name = (row.get("candidate_name") or candidate_id).strip()
            weight = parse_float(row.get("clue_weight", ""), "clue_weight", row_number)
            score = parse_float(
                row.get("match_score_minus2_to_plus2", ""),
                "match_score_minus2_to_plus2",
                row_number,
            )
            if score < -2 or score > 2:
                raise ValueError(f"row {row_number}: match score must be between -2 and +2")
            weighted = weight * score
            totals[candidate_id] += weighted
            names[candidate_id] = candidate_name
            if score > 0:
                positive[candidate_id] += 1
            elif score < 0:
                negative[candidate_id] += 1
            if score == -2:
                contradictions[candidate_id] += 1

    if not totals:
        print("No scored candidate rows found.")
        return 0

    ranked = sorted(totals, key=lambda key: totals[key], reverse=True)
    print("candidate_id\tcandidate_name\tweighted_total\tpositive\tnegative\tdirect_contradictions")
    for candidate_id in ranked:
        print(
            f"{candidate_id}\t{names[candidate_id]}\t{totals[candidate_id]:.2f}"
            f"\t{positive[candidate_id]}\t{negative[candidate_id]}\t{contradictions[candidate_id]}"
        )
    print("\nScores organize evidence; they do not override a direct contradiction or missing geometry.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize a visual investigation directory")
    init_parser.add_argument("case_dir", type=Path)
    init_parser.add_argument("--force", action="store_true", help="overwrite existing template files")

    score_parser = subparsers.add_parser("score", help="aggregate a filled candidate matrix")
    score_parser.add_argument("matrix", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "init":
            return init_case(args.case_dir, args.force)
        if args.command == "score":
            return score_candidates(args.matrix)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
