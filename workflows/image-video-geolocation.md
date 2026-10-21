# Image, Video, and Geolocation Workflow

Match the investigation to the requested precision. A similar object, a nearby
address or a single ambiguous sign is a lead, not proof of an exact scene.
Follow [execution modes](../references/execution-modes.md) for budgets and ending
outcomes, and the [common convergence gate](../references/hypothesis-convergence.md)
for precise, verified conclusions. The stages below are coverage guidance, not
a mandatory sequence of tool calls or documents.

## Choose the required precision

| Requested result | Required visual work |
|---|---|
| **Coarse:** country, region, city, broad date range, or a provenance lookup | Brief full-frame inspection; prioritize clear, discriminating clues; verify only what supports the requested granularity. Do not require street geometry or an exhaustive candidate matrix. |
| **Precise:** exact venue, building, street, coordinates, object identity, camera direction, or exact time | Establish exact-scene/object identity, relevant independent evidence mechanisms, and the spatial or temporal relationship actually requested. Test the strongest plausible near-match or contradiction. |

A coarse task may still need deep investigation if evidence is ambiguous.
A direct authoritative source may resolve a precise question cheaply when it
identifies the exact depicted scene and the required relationship. Mode controls
effort; requested precision controls the proof needed. People-related safety and
official wanted/fugitive activation gates are never relaxed by either choice.

## 1. Define and inspect the target

Identify the requested granularity, relevant date and viewpoint relationship.
“Where is the statue?” differs from “which street is behind the photographer?”
An upload date differs from a capture date. Use the supplied context without
creating a formal intake record for a simple lookup.

Preserve the original. Prefer its bytes to a screenshot when available. Inspect
metadata, edit/export signals or keyframes when they can answer or falsify the
question. Record hashes, dimensions and transformations for a reproducible case
or when provenance is disputed; do not require a separate file operation for
every ordinary visual lookup. Missing metadata does not establish fabrication.

## 2. Inspect before committing to a hypothesis

Start with a brief full-frame pass: foreground/background, permanent objects,
text, roads, terrain, occlusion, reflections and obvious contradictions. Then
inspect the most informative regions, often two or three, as needed. Record raw
observations separately from interpretations and retain consequential ambiguity.

Expand to a grid, additional crops or the full
[visual clue taxonomy](../references/visual-clue-taxonomy.md) only when the scene
is complex, the first clues conflict, a search stalls, or unexamined regions may
change the answer. Do not create a crop or record for every visible object.

Useful clue families include text/language, symbols, vehicle format, roads,
architecture, distinctive objects, commerce, landscape, ecology, illumination,
provenance and expected-but-absent features. Choose families for their ability to
distinguish candidates; no minimum family count applies to every task.

Use [the clue inventory](../templates/visual-clue-inventory.csv) when a persistent
record is useful. Otherwise keep short notes on the strongest clues, important
alternate readings, contradictions and next useful check. Numerical scoring is
optional when it helps compare many clues; it is not a prerequisite to searching.

### Ambiguous text and structured carriers

- Compare important OCR readings with the original and a targeted crop. Keep
  uncertain characters explicit, such as `NE?` or `[A/O]`.
- Use perspective correction, rotation or channel/contrast views when they
  address a specific recognition failure. Generated pixels are not evidence.
- Search alternate readings only when they could change the candidate set;
  do not expand every unreadable character into a query branch.
- For QR codes, barcodes, layers or puzzle-like carriers, use the structured
  carrier protocol in the common convergence reference. Preserve reproducible
  payloads and test relevant source-signaled transformations.

Use only the minimum vehicle-plate information needed for geographic
classification. Do not publish a complete private plate or identify a private
person by face.

## 3. Search for discriminating evidence

Choose the action most likely to resolve a material uncertainty: an original
source lookup, exact-object comparison, administrative clue, provenance check,
or map relationship. Use [adaptive strategy](../references/adaptive-investigation-strategy.md)
at a consequential branch or stall; do not rehearse a strategy table before each
search.

Separate evidence mechanisms when needed to avoid confirmation bias. Text,
object, administrative, built-environment, landscape and provenance searches are
available lanes, not six required searches. Use another reverse-image engine
only if its coverage can add useful evidence. Batch independent checks when the
host tools support it; dependent checks wait for the evidence they need.

Keep a credible alternative when ambiguity exists. Do not invent two to five
candidates after a direct exact match. For each live candidate, keep only its
support, strongest contradiction and cheapest decisive test. Use
[the candidate matrix](../templates/location-candidate-matrix.csv) for genuinely
complex comparisons; do not score every candidate against every minor clue.

Multiple pages copying an article, reposting one photograph or using one address
database count as one lineage. Prefer evidence with distinct mechanisms, such as
an exact scene photograph and a map relationship. A higher page count alone does
not increase confidence.

## 4. Verify the requested relationship

For a coarse answer, verify the geographic or temporal discrimination needed for
that answer and bound anything finer. Do not infer an exact street merely because
the city is supported.

For a precise location or viewpoint, stop broad search when a candidate is strong
enough to test directly. Compare exact object shape, wear, plaque placement,
façade sequence and stable surroundings. Verify the geometry relevant to the
question: object and camera positions, road/path order, camera side or heading,
and whether a nearby mailing address describes the street actually asked for.

Use the smallest suitable spatial evidence set: official map, street imagery,
satellite view, building footprint, address record or another documented view.
An authoritative source that directly resolves the exact scene and relationship
can be sufficient; otherwise combine independent mechanisms. Do not require
every available map type or additional imagery dates without a relevant reason.

Test the strongest plausible near-match or contradiction before a precise
conclusion. Examples include a duplicate statue, an incompatible road layout, an
opposite entrance, or a missing feature that should be visible. This can be part
of the exact-scene comparison rather than a separate tool call. Additional
adversarial checks are warranted by remaining uncertainty, not a fixed quota.

When time matters, distinguish capture, upload/publication, event and archive
times. Choose date evidence that addresses the question, such as construction
history, an event record or provenance. Shadows, weather and vegetation are
additional tests when useful, not mandatory lanes. Report a range when exact time
is unsupported.

## 5. Conclude at supported precision

Apply the common convergence gate with these visual additions only where
relevant: exact-scene identity, independent evidence mechanisms, requested
geometry/time, and the strongest credible near-match. Confidence follows the
weakest necessary link.

If evidence supports only a city when the user asked for a street, report that
boundary and the missing discriminator under the execution-mode ending rules.
Do not keep collecting solely to satisfy a checklist count.

Default output: answer and confidence, the decisive evidence with sources,
relevant geometry/time explanation, and material uncertainty or contradiction.
Add a clue inventory, candidate comparison or full geolocation report only when
the complexity or requested deliverable warrants it.

When side-by-side images would make the evidence easier to assess, or the user
requests one, optionally create a [visual evidence board](../references/visual-evidence-board.md)
from already inspected local images. Include sources, specific matches and material
uncertainties. A map is useful only when it tests the relevant spatial relationship;
do not collect extra imagery just to fill panels. A building match does not verify
the camera position, and the board must keep that distinction visible. Skip the
board when a short answer suffices or it would consume the remaining search budget.

## Boundaries

- Do not identify a private person by face.
- Do not infer or reveal a private residence or live location. Any official
  wanted/fugitive exception requires its dedicated activation and safety gates.
- Do not publish complete private vehicle plates.
- AI geolocation, OCR and visual similarity are leads and require verification.
