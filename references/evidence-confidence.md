# Evidence and Confidence Rubric

Use this rubric to label evidence; use the
[common convergence gate](hypothesis-convergence.md#common-convergence-gate) for
precise verified conclusions and [execution modes](execution-modes.md) for ending
outcomes. Confidence is a description of support, not a reason to keep collecting
after the user's question has been adequately answered.

## Source classes

- **Primary authoritative:** official registry, court filing, regulator,
  organization statement, original media or directly observed technical record.
- **Primary non-authoritative:** eyewitness post, user-uploaded media,
  self-published profile or repository commit.
- **Secondary high quality:** reporting or analysis with transparent sourcing
  and corrections.
- **Secondary aggregate:** scraped indexes, automated enrichers or databases
  whose underlying records need verification.
- **Community / anonymous:** reposts, unattributed screenshots or anonymous claims.

Authority is claim-specific: an official statement establishes what its publisher
said, but may not independently establish a disputed underlying event.

## Assess material uncertainty

Check the producer, original source/lineage, relevant time, identity consistency
and direct access to the claimed fact. Ask whether a credible alternative,
contradiction or unprocessed primary artifact could change the answer.
Use these questions where they affect the claim; do not fill a questionnaire for
every source or repeat unchanged checks.

## Confidence levels

| Level | Meaning |
|---|---|
| **High** | Direct authoritative support or multiple independent reliable mechanisms; relevant identity/time resolved; no credible unbounded contradiction; reproducible support at the stated precision. |
| **Medium** | Reliable support with a material assumption, partial corroboration or unresolved ambiguity; clearly describe what remains uncertain. |
| **Low** | Indirect, stale, ambiguous or weakly sourced support, unresolved contradictions, or dependence on search coincidence; useful as a lead, not a verified conclusion. |

High confidence does not override the common convergence gate for a precise
investigative conclusion. Report the supported level of precision and any
uncertainty; do not label a candidate verified merely because it feels likely.

## Finding labels

- **Verified fact:** direct, reproducible support at the stated scope and precision.
- **Corroborated inference:** reasoning from multiple supported facts.
- **Open hypothesis:** a coherent but insufficiently tested explanation.
- **Single-source lead:** a plausible unverified lead from one source.
- **Contradicted:** credible evidence weighs against the claim.
- **Unknown:** available evidence does not resolve it.

A single authoritative source that directly answers the question can establish a
verified fact; “single-source lead” is not an automatic label for every one-source
answer. Apply labels to substantive findings where useful, not every sentence.

## Search coincidence and independence

Matching pages may descend from the same mistaken pivot. Be cautious when a
candidate originated from one number, phrase or name and subsequent searches were
shaped only to support it. Directly test material competing evidence.

Count underlying lineages and mechanisms, not domains or result counts. Reposts,
syndicated address records and copied articles do not independently corroborate
one another. An exact photograph plus a verified map relationship may add more
support than many pages quoting one tourism article.

## Minimal evidence record

For a simple lookup, keep the claim, source and supporting observation in the
working context. Add confidence or a limitation when useful.

For a persistent or auditable case, record a finding ID, claim, source URL/file,
supporting excerpt/note, label and confidence. Add source title/publisher, relevant
publication/access times, lineage, contradiction or unresolved discriminator
where those fields affect the claim or the deliverable requires them. Reuse IDs
across case notes instead of duplicating records.

## Visual/geolocation confidence

For a coarse location claim, evaluate the weakest link necessary to establish
that granularity. Do not require street geometry to support a country or city.

For a precise scene, location or viewpoint, confidence depends on observation
quality, exact object/scene identity, regional consistency, relevant spatial
geometry/time and independent evidence mechanisms. Apply the additional checks
in [the visual workflow](../workflows/image-video-geolocation.md), including the
strongest credible near-match. A nearby address is not proof of camera geometry;
OCR and AI guesses do not resolve unreadable details.

When only the city is supported, a precise street remains unknown even if the
city confidence is high. State that boundary rather than averaging confidence
across unrelated parts of the answer.
