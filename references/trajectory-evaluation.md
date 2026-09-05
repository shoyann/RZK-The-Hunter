# Strategy evaluation and v1.4 scope

## Baseline diagnosis

Baseline: v1.3.0, commit c2a82aaf289bdbd60329764b3333012b9d91075b.
Its package verifier and seven catalog tests passed before this upgrade.
No comparable model trajectories or solve-rate measurements were available.

Already present: primary-evidence queue, fastest-falsifier field, source-lineage
checks, alternate-carrier processing, time distinctions, geometry, convergence
gates and rejection rollback. Do not implement a second copy of those mechanisms.

Missing connection: the falsifier is documented in the hypothesis ledger but is
not operationally compared with the next search. Tool selection uses static
workflow stages, not current uncertainty. Existing tests measure package integrity,
not investigation behavior. Rephrased searches have no progress feedback.

## Small release architecture

| Change | Purpose / boundary |
|---|---|
| SKILL.md + hypothesis/query/image/tool routing | Consult strategy at a consequential branch decision or stall; existing safety and answer gates remain authoritative |
| adaptive-investigation-strategy.md | Qualitative next-action ranking, cheap falsifiers, representation/habitat changes, temporal and AI fidelity, deferred clues |
| strategy-checkpoint.md | Compact action alternatives, selected discriminator and deferred-clue record; use existing ledgers rather than duplicate them |
| trajectory_eval.py | Read-only audit of a recorded JSON trace; advisory stalls, repetition and hypothesis latency; never executes actions or approves a factual answer |
| test_trajectory_eval.py | Synthetic positive/negative trace regressions and CLI validation |
| behavioral-cases.json | Perturbed task/artifact packets for future matched model runs; contains no walkthrough flags |

v1.4 does not ship numeric action weights, automatic tool promotion, a memory
database/retriever, or an autonomous benchmark runner. Those need evidence of
benefit before adding architecture. Small transferable strategy examples are
guidance, not a claim that procedural retrieval has been implemented.

## Trace format (schema_version 1)

A JSON object contains `schema_version`, `case_id`, `requirements`, and `actions`.
Requirements are answer-gate checks that apply to this case: `geometry`,
`temporal`, `carrier_complete`. An empty list is valid; the three base checks
`primary_resolved`, `direct_support`, `falsification` always apply.
An assessor, not the proposed answer, determines applicable requirements.

Every action records:

- `id` (unique), `kind` (search/verify/falsify/pivot/meta_search/transform/finalize),
  `objective`, `representation`, `habitat`, `query_family` (empty if none);
- `hypothesis` (ID or empty), `expected_discriminator`, `outcome`;
- `source_clusters`: underlying source-lineage IDs, not merely hostnames;
- `evidence_refs`: local artifact/record pointers or public source URLs;
- `progress`: observed changes, not planned actions. Allowed labels:
  new_primary, new_identifier, candidate_narrowed, confidence_changed,
  contradiction, new_discriminator, decisive.

Progress labels require both an outcome and evidence references. A new query,
representation, habitat or tool is only a procedural change, not substantive
progress by itself. References permit auditing; their presence does not prove
truth, independence or that a page was actually read.

Optional fields:

- `hypothesis_status`: open/leading/contradicted/verified; requires hypothesis ID.
- `contradicts`: IDs affected by the recorded contradiction.
- `resolves`: IDs whose outstanding contradiction was explicitly resolved by
  evidence (requires confidence_changed progress and evidence references).
  A mere verified label never clears a contradiction automatically.
- `checks`: answer-gate labels mapped to booleans on a finalize action.
  Missing/false checks produce unsupported-finalization warnings.

Distinguish raw excerpts, interpretations and strategic notes in the existing
evidence/hypothesis ledgers. The trace links them; it is not a replacement.
Never store credentials, private messages or unrelated personal data.

## Reading the audit

```bash
python scripts/trajectory_eval.py case/trajectory.json
python scripts/trajectory_eval.py case/trajectory.json --window 5 --strict
python -m unittest discover -s tests -v
```

The window is a configurable advisory sensitivity (default 3), not an instruction
to abandon a branch after three steps. Consecutive actions without substantive
progress trigger STALLED. A documented method change can be appropriate even
while the evidence state remains stalled.

Metrics:

- progress actions / all recorded actions (not tokens or elapsed time);
- repeated search ratio: same family + representation + habitat, with no new
  source cluster and no substantive progress, divided by all search actions;
- actions to first recorded decisive evidence (one-based), or null;
- leading-to-contradicted action distances, unresolved leading IDs, and
  contradiction-response action distances (downgrade or evidenced resolution). These are observed latencies, not
  proof that a hypothesis was objectively false;
- count of procedural representation/habitat changes and finalization warnings.

Empty traces return INSUFFICIENT_DATA, zero counts and null ratios. Unknown
fields, invalid booleans, duplicate IDs and unknown schema versions fail input
validation. Default exit 0 means the audit ran, not that a case is solved;
--strict exits 1 for advisory findings; invalid input exits 2.

## Behavioral evaluation protocol

The checked-in fixtures test an **annotated-trace auditor**, not a language
model's actual investigation or end-to-end solving ability. Never report their
pass rate as solve rate. A trace with all checks true is still only self-report.

For genuine v1.3/v1.4 comparison:

1. Use the raw packets in tests/fixtures/behavioral-cases.json; keep assessor
   expectations out of the investigator prompt. Perturb names/dates/coordinates.
2. Fix model, tools, allowed side effects, source snapshots, token/action budget
   and retry policy. Use a fresh context per case and variant.
3. Run the identical cases with v1.3, then v1.4 strategy. Save full tool outputs,
   final response, source availability and trajectory. Do not replay fictional
   traces as if they were observed baseline runs.
4. An independent assessor checks actual artifacts, action ordering, exact-target
   support and time/geometry/carrier requirements before assigning progress labels.
5. Report per-case accuracy and unsupported finalizations, branch/contradiction
   latency, repetition and actions to decisive evidence. Report unresolved cases
   and source loss separately; do not exclude failures silently.
6. If authorized submissions exist, separate factual accuracy from challenge
   acceptance and format errors. Never brute-force answer strings.

Add ablations only for components that exist: baseline; strategy only; strategy
plus advisory trace feedback. Future memory/retrieval, numeric ranking and dynamic
tool discovery each need their own matched ablation and overhead measurement.

## Risks and release claims

False stalls: a long extraction can be necessary; annotate why it is worth
continuing. Empty search results or access loss do not falsify an identity.
Overhead: checkpoint at branch decisions, not every click. Rigidity: ranking is
explainable and overrideable. Contamination: promote methods, not case answers or
unverified associations. Safety: no new collection permissions are introduced.

This release provides strategy guidance and testable auditing infrastructure.
**End-to-end improvement, baseline trajectories and ablation results remain
unmeasured.** Do not claim review of the entire external walkthrough corpus.
