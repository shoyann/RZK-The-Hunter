#!/usr/bin/env python3
"""Read-only, advisory audit of annotated investigation actions; never verifies truth."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

KINDS = {"search", "verify", "falsify", "pivot", "meta_search", "transform", "finalize"}
PROGRESS = {"new_primary", "new_identifier", "candidate_narrowed", "confidence_changed",
            "contradiction", "new_discriminator", "decisive"}
BASE_CHECKS = {"primary_resolved", "direct_support", "falsification"}
OPTIONAL_CHECKS = {"geometry", "temporal", "carrier_complete"}
STATUSES = {"open", "leading", "contradicted", "verified"}
TEXT_FIELDS = {"id", "kind", "objective", "representation", "habitat", "query_family",
               "hypothesis", "expected_discriminator", "outcome"}
LIST_FIELDS = {"source_clusters", "evidence_refs", "progress"}
EXTRA_FIELDS = {"hypothesis_status", "contradicts", "resolves", "checks"}


def strings(value, label):
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ValueError(f"{label} must be a list of nonempty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} contains duplicates")
    return value


def validate_trace(trace):
    if not isinstance(trace, dict):
        raise ValueError("trace must be an object")
    required = {"schema_version", "case_id", "requirements", "actions"}
    if set(trace) != required:
        raise ValueError(f"trace fields must be exactly {sorted(required)}")
    if type(trace["schema_version"]) is not int or trace["schema_version"] != 1:
        raise ValueError("unsupported schema_version; expected integer 1")
    if not isinstance(trace["case_id"], str) or not trace["case_id"].strip():
        raise ValueError("case_id must be a nonempty string")
    requirements = strings(trace["requirements"], "requirements")
    if set(requirements) - OPTIONAL_CHECKS:
        raise ValueError("unknown case requirement")
    if not isinstance(trace["actions"], list):
        raise ValueError("actions must be a list")
    seen = set()
    finalized = False
    for index, row in enumerate(trace["actions"], start=1):
        label = f"action {index}"
        if not isinstance(row, dict):
            raise ValueError(f"{label} must be an object")
        missing = (TEXT_FIELDS | LIST_FIELDS) - row.keys()
        if missing:
            raise ValueError(f"{label} missing fields: {sorted(missing)}")
        unknown = row.keys() - TEXT_FIELDS - LIST_FIELDS - EXTRA_FIELDS
        if unknown:
            raise ValueError(f"{label} unknown fields: {sorted(unknown)}")
        for field in TEXT_FIELDS:
            if not isinstance(row[field], str):
                raise ValueError(f"{label}.{field} must be a string")
            if field not in {"hypothesis", "query_family"} and not row[field].strip():
                raise ValueError(f"{label}.{field} cannot be empty")
        if row["kind"] not in KINDS:
            raise ValueError(f"{label} unknown action kind")
        if finalized:
            raise ValueError(f"{label} cannot follow a finalize action")
        if row["kind"] == "finalize":
            finalized = True
        if row["kind"] == "search" and not row["query_family"].strip():
            raise ValueError(f"{label} search requires query_family")
        if row["id"] in seen:
            raise ValueError(f"{label} duplicate action id")
        seen.add(row["id"])
        for field in LIST_FIELDS:
            strings(row[field], f"{label}.{field}")
        if set(row["progress"]) - PROGRESS:
            raise ValueError(f"{label} unknown progress label")
        if row["progress"] and not row["evidence_refs"]:
            raise ValueError(f"{label} progress requires evidence_refs")
        if "hypothesis_status" in row:
            if (not isinstance(row["hypothesis_status"], str)
                    or row["hypothesis_status"] not in STATUSES
                    or not row["hypothesis"].strip()):
                raise ValueError(f"{label} status requires valid status and hypothesis ID")
        if "contradicts" in row:
            strings(row["contradicts"], f"{label}.contradicts")
            if row["contradicts"] and "contradiction" not in row["progress"]:
                raise ValueError(f"{label} contradicts requires evidenced contradiction progress")
        if "checks" in row:
            checks = row["checks"]
            if row["kind"] != "finalize" or not isinstance(checks, dict):
                raise ValueError(f"{label} checks only allowed as an object on finalize")
            if checks.keys() - BASE_CHECKS - OPTIONAL_CHECKS:
                raise ValueError(f"{label} unknown finalization check")
            if any(type(value) is not bool for value in checks.values()):
                raise ValueError(f"{label} checks require actual booleans")
        if "resolves" in row:
            strings(row["resolves"], f"{label}.resolves")
            if row["resolves"] and ("confidence_changed" not in row["progress"]):
                raise ValueError(f"{label} resolves requires evidenced confidence_changed progress")
    return trace


def audit(trace, window=3):
    validate_trace(trace)
    if type(window) is not int or window < 1:
        raise ValueError("window must be a positive integer")
    rows = trace["actions"]
    warnings = []
    no_progress = progress_actions = repeats = searches = 0
    representation_changes = habitat_changes = 0
    decisive = None
    query_history = {}
    leading = {}
    contradictions = {}
    leading_latencies = []
    response_latencies = []
    unsupported = 0
    previous = None

    for index, row in enumerate(rows, start=1):
        progress = bool(row["progress"])
        if progress:
            progress_actions += 1
            no_progress = 0
        else:
            no_progress += 1
        if no_progress == window:
            warnings.append({"code": "STALLED", "action": row["id"],
                             "detail": f"{window} actions without evidenced substantive progress"})
        if "decisive" in row["progress"] and decisive is None:
            decisive = index
        if previous:
            representation_changes += row["representation"] != previous["representation"]
            habitat_changes += row["habitat"] != previous["habitat"]
        previous = row

        if row["kind"] == "search":
            searches += 1
            key = (row["query_family"], row["representation"], row["habitat"])
            sources = set(row["source_clusters"])
            if key in query_history and not (sources - query_history[key]) and not progress:
                repeats += 1
            query_history.setdefault(key, set()).update(sources)

        for hypothesis in row.get("contradicts", []):
            contradictions.setdefault(hypothesis, index)
        hypothesis = row["hypothesis"]
        status = row.get("hypothesis_status")
        if status == "leading":
            leading.setdefault(hypothesis, index)
        elif status in {"open", "contradicted", "verified"}:
            start = leading.pop(hypothesis, None)
            if start is not None and status == "contradicted":
                leading_latencies.append(index - start)
            if status in {"open", "contradicted"} and hypothesis in contradictions:
                response_latencies.append(index - contradictions.pop(hypothesis))
        # Verification does not silently clear a recorded unresolved contradiction.
        for resolved in row.get("resolves", []):
            if resolved not in contradictions:
                raise ValueError(f"{row['id']} resolves an unknown or already handled contradiction")
            response_latencies.append(index - contradictions.pop(resolved))

        if row["kind"] == "finalize":
            needed = BASE_CHECKS | set(trace["requirements"])
            missing = sorted(check for check in needed if not row.get("checks", {}).get(check))
            if missing or contradictions:
                unsupported += 1
                warnings.append({"code": "UNSUPPORTED_FINALIZATION", "action": row["id"],
                                 "missing_checks": missing,
                                 "unresolved_contradictions": sorted(contradictions)})

    return {
        "schema_version": 1,
        "case_id": trace["case_id"],
        "advisory_only": True,
        "strategy_state": ("INSUFFICIENT_DATA" if not rows else
                           "STALLED" if no_progress >= window else "ACTIVE"),
        "window": window,
        "metrics": {
            "actions": len(rows),
            "progress_actions": progress_actions,
            "progress_ratio": progress_actions / len(rows) if rows else None,
            "search_actions": searches,
            "repeated_searches": repeats,
            "search_repetition_ratio": repeats / searches if searches else None,
            "representation_changes": representation_changes,
            "habitat_changes": habitat_changes,
            "actions_to_decisive_evidence": decisive,
            "leading_to_contradicted_actions": leading_latencies,
            "unresolved_leading": sorted(leading),
            "contradiction_response_actions": response_latencies,
            "unresolved_contradictions": sorted(contradictions),
            "unsupported_finalizations": unsupported,
        },
        "warnings": warnings,
        "limitations": "Annotated self-report audit only; does not verify source truth, "
                       "actual tool use, requirement completeness, or model solve rate.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("--window", type=int, default=3, help="advisory no-progress window")
    parser.add_argument("--strict", action="store_true", help="exit 1 when audit warnings exist")
    args = parser.parse_args()
    try:
        result = audit(json.loads(args.trace.read_text(encoding="utf-8-sig")), args.window)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.strict and result["warnings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
