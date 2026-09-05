# Hypothesis Convergence and Retry Control

This reference prevents premature convergence: the failure mode where a plausible lead accumulates enough thematic matches to feel correct before the original evidence has been exhausted.

The goal is not to maximize the number of clues supporting a candidate. The goal is to reach a state where the best explanation survives direct evidence, contradiction checks, and deliberate attempts to falsify it.

## Core principle

A plausible explanation is not submission-safe while material first-party evidence remains unresolved.

Search results are especially dangerous when they create a dense cluster of matching details. A cluster can still be wrong if every match descends from one mistaken pivot or if a stronger original artifact has not yet been processed.

Use this order of authority unless the task context clearly requires otherwise:

1. Original artifact or authoritative primary record
2. Direct first-party source or embedded resource
3. Independent primary evidence
4. High-quality secondary reporting
5. Search/discovery results and aggregators
6. Thematic similarity, coincidence, or analyst intuition

A lower layer can generate a hypothesis. It should not overrule an unresolved higher layer.

## Investigation state machine

Track the case through these states:

### `COLLECTING`

Primary evidence is still being enumerated or processed.

Final-answer status: **blocked**.

### `HYPOTHESIZING`

At least one explanation exists, but material discriminators remain unresolved.

Final-answer status: **blocked**.

### `FALSIFYING`

A leading hypothesis exists and is being attacked with contradiction searches, alternate transformations, competing candidates, or direct checks.

Final-answer status: **blocked**.

### `CONVERGED`

The leading explanation survives the mandatory gate and no unresolved primary evidence could plausibly overturn it.

Final-answer status: **allowed**.

### `REOPENED`

A rejection, contradiction, or newly discovered artifact invalidated the previous convergence state.

Final-answer status: **blocked** until the gate passes again.

## Primary-evidence queue

At intake, enumerate every first-party artifact or direct path that may contain material evidence.

Examples:

- original image/video/audio/document;
- attachments and embedded files;
- source-provided URLs;
- HTML source, scripts, metadata, favicon, feeds, URL fragments, downloadable assets;
- archive captures and original versions;
- structured carriers such as QR/barcodes;
- alternate pages/views explicitly signaled by the source;
- source-signaled transformations such as rotate, mirror, invert, decode, inspect source, inspect metadata, or compare versions.

For each item record:

- identifier;
- why it may matter;
- status: `unprocessed`, `processed`, `blocked`, `irrelevant`;
- transformation attempts performed;
- outputs produced;
- whether it can falsify the leading hypothesis.

Do not silently drop an item because another branch produced a plausible answer.

## Structured visual carrier protocol

When the artifact is a QR code, barcode, steganographic layout, layered graphic, or puzzle-like visual carrier:

1. Preserve the original bytes and dimensions.
2. Decode the original orientation.
3. If the source or structure suggests transformation, test relevant rotations, mirror states, inversion, threshold/channel variants, and alternate layers.
4. Record every reproducible payload independently.
5. Treat multiple valid payloads as parallel evidence branches until their roles are resolved.
6. A valid first payload does **not** prove the carrier has been exhausted.

Do not perform arbitrary combinatorial image mutations without a reason. Transformations should be source-signaled, structurally motivated, or cheap enough to be a standard sanity sweep.

## Hypothesis ledger

Each candidate explanation should have an explicit record:

| Field | Meaning |
|---|---|
| ID | `H1`, `H2`, ... |
| Claim | What the hypothesis says |
| Status | `open`, `leading`, `contradicted`, `verified` |
| Supporting evidence | Direct support only |
| Contradictions | Evidence against it |
| Untested primary evidence | Items that could overturn it |
| Independence | Whether supporting clues come from distinct mechanisms |
| Fastest falsifier | Cheapest decisive test |
| Confidence | low / medium / high |

A hypothesis cannot be `verified` merely because search results produce many matching details.

Before expanding a leading branch, turn its fastest falsifier into a concrete
candidate action and execute it or document why it is deferred. Record result
and belief change separately; an inaccessible or inconclusive check is not
disproof. Use [adaptive strategy](adaptive-investigation-strategy.md) to compare
actions. The states above describe evidence readiness, not a mandatory linear
search order; strategy can move among methods while the answer gate stays closed.

## Search-coincidence hazard

Treat a candidate as vulnerable to coincidence when any of these are true:

- it was generated from one distinctive number, phrase, date, or name;
- several supporting pages copy the same source;
- later details were searched specifically to fit the candidate;
- the candidate explains secondary clues but not the original artifact;
- a material first-party branch remains unprocessed;
- the answer format is being guessed while the underlying claim is still uncertain.

When this hazard is present, lower confidence and return to falsification.

## Mandatory convergence gate

A final answer is submission-safe only when all boxes are checked:

- [ ] The exact task and required output format are understood.
- [ ] Material first-party artifacts are processed or explicitly bounded.
- [ ] Source-signaled alternate representations/transformations are resolved.
- [ ] The leading hypothesis has direct support, not only thematic or search similarity.
- [ ] Supporting evidence includes independent mechanisms where appropriate.
- [ ] At least one deliberate falsification attempt was performed.
- [ ] The second-best explanation or unresolved alternative was tested enough to reject or bound it.
- [ ] Credible contradictions are resolved or reflected in confidence.
- [ ] No unresolved primary evidence could plausibly overturn the answer.
- [ ] The final wording is derived from the evidence or task format, not guessed by repeated mutation.

If any material box is unchecked, return a provisional finding and the next discriminator instead of a precise final answer.

## Rejection loop

A rejected answer is not permission to brute-force wording.

When an answer is rejected:

1. Record the exact submitted answer and rejection.
2. Separate **claim failure** from **format failure**.
3. Do not assume format failure unless the underlying claim already passed the convergence gate.
4. Roll back to the last verified checkpoint.
5. Mark hypotheses affected by the rejection.
6. Reopen unprocessed first-party evidence and alternate branches.
7. Change one assumption at a time.
8. Run the cheapest falsifier.
9. Re-enter the convergence gate.

This mirrors a software-engineering agent loop:

`attempt -> test -> failure -> inspect -> revise one assumption -> retest -> converge`

The investigation equivalent is:

`hypothesis -> evidence test -> contradiction/rejection -> rollback -> reopen evidence -> falsify -> reconverge`

## Stop conditions

Stop and report uncertainty when:

- the decisive primary source is inaccessible through lawful means;
- remaining branches are indistinguishable with available evidence;
- additional collection would be disproportionate, invasive, or outside scope;
- the answer depends on private or restricted data not authorized for use.

A disciplined unresolved result is better than a confident false positive.

## Minimal reporting block

For multi-stage investigations, include:

- **Current state:** collecting / hypothesizing / falsifying / converged / reopened
- **Leading hypothesis:** claim + confidence
- **Unprocessed primary evidence:** count or list
- **Strongest contradiction:** one line
- **Fastest falsifier:** one line
- **Submission-safe:** yes / no
