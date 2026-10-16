# Hypothesis Convergence and Retry Control

Use this reference for ambiguous or multi-stage investigations and for precise
conclusions that need a deliberate verification gate. It defines the common
detailed evidence gate; scenario workflows add only their relevant checks.
[Execution modes](execution-modes.md) define effort, checkpoints and ending
outcomes. A failed evidence gate does not require unlimited investigation.

## Core principle

A plausible lead is not a precise verified answer while known material evidence
could overturn it. Prefer original artifacts and authoritative primary records,
then direct first-party sources, independent primary evidence, reliable secondary
reporting, and finally discovery results. Matching search results from one
lineage do not outweigh a conflicting original artifact.

“Material” means capable of changing the answer to the user's actual question.
It does not mean every linked page, embedded asset or imaginable transformation.
Bound irrelevant or inaccessible evidence with a short reason.

## Evidence readiness and ending outcomes

These readiness states may be useful for a complex case; do not create a state
log for every simple lookup.

| Readiness | Meaning |
|---|---|
| `COLLECTING` | Material primary evidence is still being processed. |
| `HYPOTHESIZING` | A candidate exists but necessary discriminators are unresolved. |
| `FALSIFYING` | The leading claim is being tested against a credible contradiction or alternative. |
| `CONVERGED` | The applicable evidence gate passes at the requested precision. |
| `REOPENED` | New material evidence or rejection invalidated a previous conclusion. |

Readiness describes evidence, not whether the turn may end. A case still
collecting or falsifying can end as `bounded_uncertain` or `blocked` under the
execution-mode rules. It must not present an unverified precise answer as resolved.
These terms do not change the version-1 trajectory audit schema or its states.

## Primary evidence and hypotheses

For a multi-stage case, keep a compact queue of unresolved material artifacts:
supplied originals, direct URLs, relevant embedded resources, metadata, archives,
attachments or source-signaled alternate views. Record the item, why it matters,
status (`unprocessed`, `processed`, `blocked`, `irrelevant`) and decisive result.
Link existing notes rather than copying excerpts into multiple records.

Keep only live hypotheses and meaningful rejected alternatives. For each, retain:
claim, direct support, strongest contradiction, untested material evidence,
cheapest decisive test and status (`open`, `leading`, `contradicted`, `verified`).
Confidence and source-lineage notes belong with the evidence they describe.
No minimum number of hypotheses or persistent files is required.

Before expanding a branch that depends on an untested anchor, test its cheapest
decisive falsifier or record a short reason for preferring another action. Reuse
a completed check when its evidence and assumptions have not changed. An
inaccessible or inconclusive test neither verifies nor disproves the hypothesis.
Consult [adaptive strategy](adaptive-investigation-strategy.md) at consequential
choices or stalls, not before every tool call.

## Structured visual carriers

For QR codes, barcodes, layered graphics or puzzle-like carriers:

1. Preserve the original bytes and decode the original representation.
2. If the source or structure signals a relevant transformation, test it:
   rotation, mirror, inversion, channel/threshold view or alternate layer.
3. Keep reproducible payloads distinct until their roles are understood.
4. Treat a first valid payload as sufficient only when no material source-signaled
   branch remains unresolved.

Do not enumerate arbitrary transformations. A cheap sanity check is appropriate
when it addresses a credible ambiguity; additional transforms need a concrete
discriminator. Apply execution-mode checkpoints to this work too.

## Common convergence gate

Before presenting a precise, verified investigative conclusion, check:

- The exact question, relevant time, requested precision and output format are understood.
- Material supplied/first-party evidence is processed or explicitly bounded.
- Relevant source-signaled alternate representations or transformations are resolved.
- The claim has direct support, not merely thematic similarity or search coincidence.
- Support uses independent evidence mechanisms where needed; copied sources count once.
- The strongest credible alternative or contradiction has been deliberately tested.
- Remaining contradictions are resolved or bounded so they cannot overturn the stated conclusion.
- No known unresolved material primary evidence could plausibly overturn that conclusion.
- The answer follows the evidence and requested format, rather than repeated answer-string guesses.

A deliberate falsification check can be part of an existing source comparison;
it need not be a separate search or tool call. A direct authoritative lookup
does not require invented alternatives or a ceremonial second source. For
precise visual or guarded work, apply the additional scenario-specific checks.
Official wanted/fugitive safety and activation gates always remain mandatory.

If a material condition is unmet, follow execution-mode continuation or ending
rules. Report the supported finding, uncertainty and next discriminator rather
than claiming precision. A bounded result must visibly retain its limitations;
it is not a bypass for calling an unsupported claim verified.

## Rejection and reopening

A rejection is evidence, not permission to brute-force wording.

1. Record the submitted claim and rejection.
2. Distinguish claim failure from a demonstrated format failure. Do not assume
   format failure while the claim is still unsupported.
3. Reopen only hypotheses, evidence items and checks affected by the rejection;
   keep unaffected verified evidence and completed checks.
4. Change one material assumption at a time and choose the cheapest decisive test.
5. Reapply the relevant gate if the evidence changes.

A wording-only rejection of an already verified claim may need a format correction,
not a fresh full investigation. A new conflict can reopen a resolved case, but
must still use the execution-mode budget and stagnation rules.

## Compact reporting

Report the answer or current supported finding, confidence, decisive source(s),
and any material limitation. For a complex unresolved case, add the leading
hypothesis, strongest contradiction and next cheapest discriminator. Include a
readiness state or evidence queue only when it helps the user continue or audit
the work. Do not duplicate the case notes in every update.
