# Execution modes and bounded completion

This is the shared authority for investigation depth, collection budgets and
completion outcomes. Specialized workflows add evidence or safety requirements;
they do not require performing unrelated stages. Read once per case, then keep
only the selected mode, next checkpoint and current evidence gap in working state.

## Choose the smallest sufficient mode

| Mode | Use when | Initial collection checkpoint | Record and deliver |
|---|---|---:|---|
| `lookup` | A narrow fact can be answered by a direct authoritative source | 2 rounds | Answer, source and any uncertainty; no case files by default |
| `standard` | A bounded claim needs source comparison or ambiguity resolved | 6 rounds | Compact findings and evidence IDs; persistent notes only when useful |
| `deep` | Linked artifacts, difficult historical reconstruction, precise geolocation, or a full investigation | 12 rounds | Evidence/hypothesis state; an audit trail or detailed report when requested/needed |

These are initial review checkpoints, not required work, guaranteed runtimes or
model-enforced limits. Stop as soon as the evidence meets the requested result.
Never search merely to use the remaining allowance. User-specified time, token,
cost or action limits take precedence and must not be exceeded. Use host-reported
usage for token limits; never estimate hidden reasoning usage from answer length.
If the host cannot expose/enforce an exact token limit, state that limitation and
use an agreed observable time/action bound rather than claiming exact enforcement.

A collection round is one external retrieval batch followed by assessing its
evidence change. Independent lookups may share a batch; a dependent follow-up is
a new round. Batching must remain relevant and proportionate, not hide hundreds
of requests inside one round. File reads, parsing and notes are not additional
collection rounds, but still consume any wall-time or total-action budget.

At the checkpoint, either finish or identify the specific unresolved discriminator,
why another bounded batch is worthwhile, and the next finite checkpoint. Continue
within the user's existing authorization only if there is useful evidence progress
or a concrete, credible discriminating test. Do not renew budgets on vague hopes,
minor query rewording or an unchanged access barrier. A user hard limit requires
reporting the current result when reached, not silently extending it.

Upgrade `lookup` to `standard` on source conflict, indirect evidence or ambiguity;
upgrade to `deep` when linked artifacts or precise geometry actually require it.
Do not upgrade just because a checklist has more fields. Guarded work always reads
the safety policy before collection; official wanted/fugitive location work is
always `deep` and must pass its dedicated activation and reporting gates.

## Detect a stall without manufacturing work

Progress means new supported evidence, a meaningful candidate reduction, a resolved
contradiction, a justified confidence change, or a newly executable discriminator.
A new website or search phrase alone is not progress.

After two consecutive collection rounds without progress, reassess the pending
falsifier, source representation and evidence habitat. Allow one justified pivot
when it has a concrete expected observation; if that also fails to produce progress
and no worthwhile test remains, finish `bounded_uncertain` (or `blocked` if a
specific dependency prevents progress). This is a review heuristic, not a claim
that every slow method is futile. A necessary long extraction may continue within
budget when its remaining work and expected evidence are concrete. Reset the
no-progress count only for an evidence change, not for renaming a query or method.

## Separate completion from certainty

| Outcome | Required basis | Return |
|---|---|---|
| `resolved` | The exact question is answered at the requested precision and applicable evidence gates pass | Finding with sources and calibrated confidence |
| `bounded_uncertain` | Useful partial findings exist, or ambiguity remains and no worthwhile authorized next action fits the remaining budget | Supported findings, unresolved claim, strongest limitation and cheapest missing discriminator |
| `blocked` | A specific unavailable source, necessary user input or access/scope constraint prevents further useful work | What is established, the blocker and the condition for resuming |

For `lookup`, a direct authoritative record can suffice after checking that it
actually supports the requested entity, field and relevant time, with no credible
contradiction. Do not invent a second hypothesis, source or separate falsification
search to satisfy a quota. Unexpected ambiguity escalates the mode instead.

For `standard`, verify material claims and address credible alternatives. Apply
the [convergence gate](hypothesis-convergence.md#common-convergence-gate) to
precise inferential conclusions with competing hypotheses or linked evidence;
straightforward directly supported subclaims need not each repeat that gate.
`deep` conclusions use that gate plus the relevant specialized requirements.
An unpassed gate may end in `bounded_uncertain` or `blocked`; it never licenses
an unsupported precise answer or requires endless investigation.

Evidence-readiness states such as `FALSIFYING` describe the hypothesis, not whether
a useful response can be delivered. These completion outcomes belong in case notes
or the report. Do not insert them as new fields/actions into the unchanged v1
trajectory audit schema or manufacture a passing `finalize` for an unresolved case.
The optional auditor may still flag a reopened case; that is advisory, not a
requirement to keep spending collection budget.

## Compact working state

Keep the current question/precision, mode and budget, leading hypothesis (if any),
evidence IDs, material contradictions, next discriminator and completion outcome.
Update only what changed. Read the needed evidence record by ID rather than
reprinting all findings. Save full artifacts outside the conversational summary.
Retain provenance, source dates and independence notes needed to audit a claim;
compression must not erase contrary evidence. No empty tables or nine-part report
are required for a lookup. Persist case files only for continuity, audit needs or
the requested deliverable. Guarded workflows retain their required handling fields.

## Operational metrics are optional

The collection heuristic is guidance, not a runtime scheduler. No automatic Codex
usage collector or model benchmark is included. If the host supplies run metrics,
record them separately in `run-metrics.jsonl`: case/run ID, model, mode, input,
cached-input, output and reasoning tokens, elapsed time, tool calls and outcome.
Unavailable counters stay null; do not add reasoning tokens to output tokens when
the provider includes them there already. Keep these records separate from the
strict v1 trajectory schema. Static prompt sizes and script tests do not establish
end-to-end speed, cost or solve-rate improvements.
