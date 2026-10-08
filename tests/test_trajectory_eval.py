import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from trajectory_eval import audit, validate_trace


def action(number, **changes):
    row = dict(id=f"A{number}", kind="search", objective="Test a public-source hypothesis",
               representation="current", habitat="web", query_family="same-target",
               hypothesis="", expected_discriminator="Differentiate alternatives",
               outcome="No relevant change", source_clusters=["origin-1"],
               evidence_refs=[], progress=[])
    row.update(changes)
    return row


def trace(*rows, requirements=()):
    return dict(schema_version=1, case_id="synthetic", requirements=list(requirements),
                actions=list(rows))


def final(number, **checks):
    return action(number, kind="finalize", query_family="", checks=dict(
        primary_resolved=True, direct_support=True, falsification=True, **checks))


class TrajectoryTests(unittest.TestCase):
    def test_empty_is_not_success(self):
        result = audit(trace())
        self.assertEqual(result["strategy_state"], "INSUFFICIENT_DATA")
        self.assertIsNone(result["metrics"]["progress_ratio"])

    def test_stall_and_rephrased_queries(self):
        result = audit(trace(*(action(n) for n in range(1, 4))))
        self.assertEqual(result["strategy_state"], "STALLED")
        self.assertAlmostEqual(result["metrics"]["search_repetition_ratio"], 2 / 3)

    def test_novel_source_not_counted_as_repeat(self):
        result = audit(trace(action(1), action(2, source_clusters=["origin-2"])))
        self.assertEqual(result["metrics"]["search_repetition_ratio"], 0)

    def test_cosmetic_pivot_does_not_reset_stall(self):
        result = audit(trace(action(1), action(2),
                             action(3, kind="pivot", representation="metadata")))
        self.assertEqual(result["strategy_state"], "STALLED")
        self.assertEqual(result["metrics"]["representation_changes"], 1)

    def test_evidenced_progress_resets_stall(self):
        result = audit(trace(action(1), action(2), action(3,
            progress=["candidate_narrowed"], evidence_refs=["fixture:table-row-4"],
            outcome="Only two catalog rows match the visible outline")))
        self.assertEqual(result["strategy_state"], "ACTIVE")
        self.assertEqual(result["metrics"]["progress_actions"], 1)

    def test_glass_monolith_latency(self):
        result = audit(trace(action(1, hypothesis="H1", hypothesis_status="leading"),
            action(2, kind="falsify", hypothesis="H1", hypothesis_status="contradicted",
                   outcome="Catalog silhouette conflicts with original",
                   evidence_refs=["fixture:outlines"], progress=["contradiction"])))
        self.assertEqual(result["metrics"]["leading_to_contradicted_actions"], [1])
        self.assertEqual(result["metrics"]["unresolved_leading"], [])

    def test_unresolved_lead_not_counted_as_killed(self):
        result = audit(trace(action(1, hypothesis="H1", hypothesis_status="leading"),
                             action(2, outcome="Page unavailable")))
        self.assertEqual(result["metrics"]["leading_to_contradicted_actions"], [])
        self.assertEqual(result["metrics"]["unresolved_leading"], ["H1"])

    def test_contradiction_latency_and_repeat_leading(self):
        result = audit(trace(action(1, hypothesis="H1", hypothesis_status="leading"),
            action(2, hypothesis="H1", hypothesis_status="leading", contradicts=["H1"],
                   progress=["contradiction"], evidence_refs=["fixture:shape"]),
            action(3, hypothesis="H1", hypothesis_status="contradicted")))
        self.assertEqual(result["metrics"]["leading_to_contradicted_actions"], [2])
        self.assertEqual(result["metrics"]["contradiction_response_actions"], [1])

    def test_decisive_evidence_index(self):
        result = audit(trace(action(1), action(2, kind="verify", progress=["decisive"],
                             evidence_refs=["fixture:original-record"])))
        self.assertEqual(result["metrics"]["actions_to_decisive_evidence"], 2)

    def test_verified_label_does_not_erase_contradiction(self):
        conflicting = action(1, hypothesis="H1", contradicts=["H1"],
                             progress=["contradiction"], evidence_refs=["fixture:source-A"])
        verified = action(2, hypothesis="H1", hypothesis_status="verified")
        result = audit(trace(conflicting, verified, final(3)))
        self.assertEqual(result["metrics"]["unsupported_finalizations"], 1)
        resolution = action(2, kind="verify", hypothesis="H1", hypothesis_status="verified",
                            resolves=["H1"], progress=["confidence_changed"],
                            evidence_refs=["fixture:source-A-correction"],
                            outcome="Original publisher corrected the conflicting field")
        result = audit(trace(conflicting, resolution, final(3)))
        self.assertEqual(result["metrics"]["unsupported_finalizations"], 0)

    def test_unknown_resolution_is_invalid(self):
        with self.assertRaises(ValueError):
            audit(trace(action(1, resolves=["H9"], progress=["confidence_changed"],
                               evidence_refs=["fixture:unrelated-record"])))

    def test_historical_carrier_and_geometry_gates(self):
        for requirement in ("temporal", "carrier_complete", "geometry"):
            with self.subTest(requirement=requirement):
                bad = audit(trace(final(1), requirements=[requirement]))
                good = audit(trace(final(1, **{requirement: True}), requirements=[requirement]))
                self.assertEqual(bad["metrics"]["unsupported_finalizations"], 1)
                self.assertEqual(good["metrics"]["unsupported_finalizations"], 0)
                self.assertNotIn("verified", good)

    def test_unknown_final_checks_not_silent(self):
        with self.assertRaises(ValueError):
            audit(trace(final(1, made_up=True)))

    def test_unsubstantiated_progress_rejected(self):
        with self.assertRaises(ValueError):
            audit(trace(action(1, progress=["decisive"])))

    def test_strict_schema_validation(self):
        mutations = [
            lambda t: t.update(schema_version=2),
            lambda t: t.update(schema_version=True),
            lambda t: t.update(requirements=["unknown"]),
            lambda t: t["actions"].append(copy.deepcopy(t["actions"][0])),
            lambda t: t["actions"][0].update(progress=["representation_changed"]),
            lambda t: t["actions"][0].update(evidence_refs="not-a-list"),
            lambda t: t["actions"][0].update(contradicts=["H1"]),
            lambda t: t["actions"][0].update(hypothesis_status="leading"),
            lambda t: t["actions"][0].update(unknown_field=True),
        ]
        for mutate in mutations:
            t = trace(action(1))
            mutate(t)
            with self.subTest(trace=t), self.assertRaises(ValueError):
                validate_trace(t)

    def test_boolean_strings_rejected(self):
        row = final(1)
        row["checks"]["direct_support"] = "true"
        with self.assertRaises(ValueError):
            audit(trace(row))

    def test_window_validation(self):
        for window in (0, -1, True):
            with self.assertRaises(ValueError):
                audit(trace(), window=window)

    def test_audit_does_not_mutate_trace(self):
        data = trace(action(1))
        before = copy.deepcopy(data)
        audit(data)
        self.assertEqual(data, before)

    def test_fixture_packets_have_distinct_raw_cases(self):
        cases = json.loads((ROOT / "tests/fixtures/behavioral-cases.json").read_text())
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        self.assertGreaterEqual(len(cases), 10)
        self.assertTrue(all(c["artifacts"] and c["request"] for c in cases))

    def test_finalization_state_before_any_conclusion(self):
        for data in (trace(), trace(action(1))):
            with self.subTest(data=data):
                result = audit(data)
                self.assertEqual(result["finalization_state"], "NOT_FINALIZED")
                self.assertIsNone(result["latest_finalization"])
                self.assertIsNone(result["active_finalization"])
                self.assertIsNone(result["reopened_at"])
                self.assertEqual(result["metrics"]["reopened_investigations"], 0)

    def test_finalization_followed_by_search_reopens_investigation(self):
        data = trace(final(1), action(2))
        before = copy.deepcopy(data)
        result = audit(data)
        self.assertEqual(data, before)
        self.assertEqual(result["strategy_state"], "ACTIVE")
        self.assertEqual(result["finalization_state"], "REOPENED")
        self.assertIsNone(result["active_finalization"])
        self.assertEqual(result["latest_finalization"], "A1")
        self.assertEqual(result["reopened_at"], "A2")
        self.assertEqual(result["metrics"]["reopened_investigations"], 1)
        self.assertEqual([w["code"] for w in result["warnings"]],
                         ["REOPENED_WITHOUT_FINALIZATION"])

    @staticmethod
    def new_contradiction(number, hypothesis="H1"):
        return action(number, kind="falsify", hypothesis=hypothesis,
                      contradicts=[hypothesis], progress=["contradiction"],
                      evidence_refs=["fixture:new-primary-record"],
                      outcome="New evidence contradicts the earlier conclusion")

    @staticmethod
    def resolve_contradiction(number, hypothesis="H1"):
        return action(number, kind="verify", hypothesis=hypothesis,
                      resolves=[hypothesis], progress=["confidence_changed"],
                      evidence_refs=["fixture:original-record-correction"],
                      outcome="Primary evidence explains the apparent contradiction")

    def test_post_finalization_contradiction_is_reported(self):
        result = audit(trace(final(1), self.new_contradiction(2)))
        self.assertEqual(result["finalization_state"], "REOPENED")
        self.assertEqual(result["metrics"]["unresolved_contradictions"], ["H1"])
        self.assertEqual(result["metrics"]["unsupported_finalizations"], 0)
        self.assertEqual(result["warnings"][0]["previous_finalization"], "A1")
        self.assertEqual(result["warnings"][0]["unresolved_contradictions"], ["H1"])

    def test_resolving_new_evidence_still_requires_new_finalization(self):
        result = audit(trace(final(1), self.new_contradiction(2),
                             self.resolve_contradiction(3)))
        self.assertEqual(result["finalization_state"], "REOPENED")
        self.assertEqual(result["metrics"]["unresolved_contradictions"], [])
        self.assertIsNone(result["active_finalization"])
        self.assertEqual(result["reopened_at"], "A2")
        self.assertEqual([w["code"] for w in result["warnings"]],
                         ["REOPENED_WITHOUT_FINALIZATION"])

    def test_reinvestigation_can_reach_a_new_finalization(self):
        result = audit(trace(final(1), self.new_contradiction(2),
                             self.resolve_contradiction(3), final(4)))
        self.assertEqual(result["finalization_state"], "FINALIZED")
        self.assertEqual(result["active_finalization"], "A4")
        self.assertEqual(result["latest_finalization"], "A4")
        self.assertIsNone(result["reopened_at"])
        self.assertEqual(result["metrics"]["reopened_investigations"], 1)
        self.assertEqual(result["warnings"], [])

    def test_multiple_reinvestigation_cycles_are_allowed(self):
        result = audit(trace(final(1), self.new_contradiction(2),
                             self.resolve_contradiction(3), final(4),
                             self.new_contradiction(5, "H2"),
                             self.resolve_contradiction(6, "H2"), final(7)))
        self.assertEqual(result["active_finalization"], "A7")
        self.assertEqual(result["finalization_state"], "FINALIZED")
        self.assertEqual(result["metrics"]["reopened_investigations"], 2)
        self.assertEqual(result["warnings"], [])

    def test_new_finalization_cannot_ignore_new_contradiction(self):
        result = audit(trace(final(1), self.new_contradiction(2), final(3)))
        self.assertEqual(result["finalization_state"], "UNSUPPORTED")
        self.assertEqual(result["latest_finalization"], "A3")
        self.assertIsNone(result["active_finalization"])
        self.assertIsNone(result["reopened_at"])
        self.assertEqual(result["metrics"]["unsupported_finalizations"], 1)
        self.assertEqual([w["code"] for w in result["warnings"]],
                         ["UNSUPPORTED_FINALIZATION"])

    def test_latest_finalization_must_supply_its_own_checks(self):
        latest = final(2)
        del latest["checks"]["direct_support"]
        result = audit(trace(final(1), latest))
        self.assertEqual(result["finalization_state"], "UNSUPPORTED")
        self.assertIsNone(result["active_finalization"])
        self.assertEqual(result["warnings"][0]["missing_checks"], ["direct_support"])
        valid = audit(trace(final(1), final(2)))
        self.assertEqual(valid["active_finalization"], "A2")
        self.assertEqual(valid["metrics"]["reopened_investigations"], 0)
        self.assertEqual(valid["warnings"], [])

    def test_refinalization_preserves_historical_warnings(self):
        unsupported = final(1)
        unsupported["checks"]["direct_support"] = False
        result = audit(trace(unsupported, action(2, kind="verify",
                             progress=["new_primary"], evidence_refs=["fixture:record"]),
                             final(3)))
        self.assertEqual(result["finalization_state"], "FINALIZED")
        self.assertEqual(result["active_finalization"], "A3")
        self.assertEqual(result["metrics"]["reopened_investigations"], 1)
        self.assertEqual([w["code"] for w in result["warnings"]],
                         ["UNSUPPORTED_FINALIZATION"])

    def test_reopening_cli_strict_exit_codes(self):
        cases = [
            (trace(final(1), self.new_contradiction(2)), 1, "REOPENED"),
            (trace(final(1), self.new_contradiction(2),
                   self.resolve_contradiction(3)), 1, "REOPENED"),
            (trace(final(1), self.new_contradiction(2),
                   self.resolve_contradiction(3), final(4)), 0, "FINALIZED"),
            (trace(final(1), self.new_contradiction(2), final(3)), 1, "UNSUPPORTED"),
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "trace.json"
            cmd = [sys.executable, str(ROOT / "scripts/trajectory_eval.py"), str(path)]
            for data, code, state in cases:
                with self.subTest(state=state, code=code):
                    path.write_text(json.dumps(data), encoding="utf-8")
                    before = path.read_bytes()
                    result = subprocess.run(cmd + ["--strict"], capture_output=True, text=True)
                    self.assertEqual(result.returncode, code, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["finalization_state"], state)
                    self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
                    self.assertEqual(path.read_bytes(), before)

    def test_cli_exit_codes_and_read_only(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "trace.json"
            data = trace(action(1), action(2), action(3))
            path.write_text(json.dumps(data), encoding="utf-8")
            before = path.read_bytes()
            cmd = [sys.executable, str(ROOT / "scripts/trajectory_eval.py"), str(path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["strategy_state"], "STALLED")
            self.assertEqual(subprocess.run(cmd + ["--strict"], capture_output=True).returncode, 1)
            self.assertEqual(path.read_bytes(), before)
            path.write_text("not json", encoding="utf-8")
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
