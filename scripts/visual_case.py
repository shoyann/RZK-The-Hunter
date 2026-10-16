#!/usr/bin/env python3
"""Initialize and score a multi-signal image/video geolocation case."""

from __future__ import annotations

import argparse
import csv
import math
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

QUICK_NOTES = """# Visual Case Notes

- Requested output and precision:
- Original source or file:
- Decisive observation and evidence reference:
- Working answer and confidence:
- Strongest relevant alternative or contradiction, and check:
- Unresolved uncertainty or next useful action:

Keep observations separate from interpretations. Add only evidence needed for the
requested answer; do not invent extra candidates to fill a quota. Escalate to
full mode if ambiguity, conflicting evidence or a precise viewpoint requires it.
Full mode adds templates without replacing these notes.

Detailed guidance when needed: workflows/image-video-geolocation.md and
references/hypothesis-convergence.md in the skill package.
"""

QUICK_CHECKLIST = """# Visual Investigation Checklist

Use only checks relevant to the requested precision; mark others not applicable.

- [ ] Requested output and available original source identified
- [ ] Answer linked to the decisive observed evidence
- [ ] Relevant ambiguity or strongest contradiction checked
- [ ] Exact identity/viewpoint, date or carrier completeness checked when required
- [ ] Confidence, limitations and remaining uncertainty stated

Escalate to full mode when the evidence needs structured comparison. Additional
candidates, crops and falsification tests need a concrete information benefit.
"""

FULL_CHECKLIST = """# Visual Investigation Checklist

Use templates and checks only where they affect the requested answer. For an
ordinary lookup, direct support and a relevant ambiguity check may be sufficient.
Exact identification requires discriminating evidence; viewpoint, historical and
multi-frame questions also need the corresponding geometry, time or carrier check.
No fixed number of clue families, candidates or falsification tests is required.

- [ ] Requested target and required precision defined
- [ ] Relevant original evidence preserved; hash if provenance needs it
- [ ] Scene observations distinguished from interpretation
- [ ] Crops or alternate OCR readings inspected where they could resolve ambiguity
- [ ] Useful clues and genuine competing candidates compared, if any
- [ ] Source lineages recorded for evidence used in the answer
- [ ] Near-match or strongest-alternative test performed for ambiguous/exact identity
- [ ] Camera/object/road geometry verified when the answer depends on viewpoint
- [ ] Relevant historical date or carrier completeness verified when required
- [ ] Contradictions and unresolved questions reported
"""


def init_case(case_dir: Path, force: bool = False, mode: str = "full") -> int:
    if mode not in {"quick", "full"}:
        raise ValueError("mode must be quick or full")
    case_dir.mkdir(parents=True, exist_ok=True)
    created = []
    skipped = []
    for output_name, template in (FILES.items() if mode == "full" else ()):
        destination = case_dir / output_name
        if destination.exists() and not force:
            skipped.append(output_name)
            continue
        shutil.copyfile(template, destination)
        created.append(output_name)

    if mode == "quick":
        notes = case_dir / "case-notes.md"
        # Notes are analyst work, not a template to reset with --force.
        if notes.exists():
            skipped.append(notes.name)
        else:
            notes.write_text(QUICK_NOTES, encoding="utf-8")
            created.append(notes.name)

    checklist = case_dir / "workflow-checklist.md"
    if not checklist.exists() or force:
        checklist.write_text(
            QUICK_CHECKLIST if mode == "quick" else FULL_CHECKLIST,
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
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"row {row_number}: invalid {field}={value!r}") from exc
    if not math.isfinite(parsed):
        raise ValueError(f"row {row_number}: {field} must be finite, got {value!r}")
    return parsed


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
            if weight < 0:
                raise ValueError(f"row {row_number}: clue_weight must be non-negative")
            score = parse_float(
                row.get("match_score_minus2_to_plus2", ""),
                "match_score_minus2_to_plus2",
                row_number,
            )
            if score < -2 or score > 2:
                raise ValueError(f"row {row_number}: match score must be between -2 and +2")
            weighted = weight * score
            if not math.isfinite(weighted):
                raise ValueError(f"row {row_number}: weighted score exceeds the finite numeric range")
            total = totals[candidate_id] + weighted
            if not math.isfinite(total):
                raise ValueError(f"row {row_number}: candidate total exceeds the finite numeric range")
            totals[candidate_id] = total
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
    init_parser.add_argument("--mode", choices=("quick", "full"), default="full",
                             help="quick notes/checklist or full templates (default: full)")
    init_parser.add_argument("--force", action="store_true", help="overwrite existing template files")

    score_parser = subparsers.add_parser("score", help="aggregate a filled candidate matrix")
    score_parser.add_argument("matrix", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "init":
            return init_case(args.case_dir, args.force, args.mode)
        if args.command == "score":
            return score_candidates(args.matrix)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
