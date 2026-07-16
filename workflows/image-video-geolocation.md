# Image, Video, and Geolocation Workflow

The objective is not to find one plausible clue. It is to build a **multi-signal explanation** in which the visible scene, the candidate location, and the exact wording of the question all agree.

A search result is a lead. A visually similar object is a lead. An address near the object is a lead. None of these alone establishes the requested street, building, date, or camera position.

## Default evidence contract

Unless one authoritative primary source resolves the exact question directly, do not submit a precise location from a single clue or a single source lineage.

For a high-confidence exact-location answer, normally require:

- at least **three distinct clue families** collected from the media;
- at least **two independent clue families** supporting the city or region;
- an exact-object or exact-scene match when a distinctive object is central to the task;
- a **geometric verification** for the requested street/building/direction using maps, street-level imagery, satellite, parcel/address data, or an equivalent spatial source;
- no unresolved high-value contradiction;
- at least two deliberate attempts to falsify the leading candidate.

A primary source that explicitly identifies the exact depicted object and its precise position can reduce the number of required sources, but it does not remove the need to answer the question's geometry correctly.

## Stage 0 — Define the exact target

Rewrite the task as a testable output before searching.

Examples:

- “Identify the city” is different from “name the street behind the photographer.”
- “Where is the statue located?” is different from “which road is visible beyond the statue?”
- “When was the image posted?” is different from “when was the scene photographed?”

Record:

- requested granularity: country / city / venue / street / building / coordinates / time range;
- viewpoint relationship: in front of, behind, across from, reflected in, viewed through;
- acceptable uncertainty;
- what would constitute a complete answer.

## Stage 1 — Preserve and inspect the original

1. Preserve the original file; do not begin from a screenshot if the original is available.
2. Record filename, dimensions, format, byte size, color profile, and cryptographic hash.
3. Inspect EXIF/XMP/IPTC/container metadata and edit/export history signals.
4. Note whether metadata is absent, stripped, internally inconsistent, or inherited from a repost.
5. For video, extract representative keyframes and preserve timestamps relative to the clip.

Metadata is evidence only when its provenance is trustworthy. Missing metadata is not evidence that an image is fabricated.

## Stage 2 — Exhaustive clue harvest before web searching

**Do not commit to a location hypothesis yet.** First inventory the entire frame.

Use two passes:

### Pass A: full-frame scene model

Describe the scene without naming a place:

- environment and land use;
- foreground, middle ground, and background layers;
- likely camera position and viewing direction;
- occlusions, reflections, cropping, and perspective;
- which elements are permanent, semi-permanent, or transient.

### Pass B: systematic region sweep

Inspect a 3×3 or 4×4 grid plus semantic crops. Create crops for every information-bearing region, not only the most obvious sign.

Record each clue in `templates/visual-clue-inventory.csv`. Preserve the raw observation before interpretation.

Required clue families:

| Family | Examples |
|---|---|
| Text and language | signs, plaques, storefronts, posters, partial letters, diacritics, typography |
| Symbols and heraldry | flags, coats of arms, seals, logos, uniforms, religious or civic symbols |
| Vehicles | registration format, regional prefix, inspection stickers, vehicle fleet, driving side |
| Roads and transport | lane markings, curbs, bollards, tram wires, bus-stop design, rails, paving |
| Architecture | roof form, façade, windows, balconies, materials, building age, setbacks |
| Public realm | benches, lamps, bins, planters, fences, utility cabinets, street furniture |
| Named or distinctive objects | statues, murals, monuments, sculptures, playgrounds, bridges |
| Commerce and institutions | business type, menus, awnings, hotel/clinic/school cues, opening-hours format |
| Physical geography | coastline, lake, river, relief, soil, rock, skyline, horizon |
| Ecology and season | tree species, vegetation, leaf state, landscaping, snow, agricultural pattern |
| Weather and illumination | cloud type, wetness, shadow direction, sun elevation, artificial lighting |
| Human activity | clothing, event context, tourism patterns, mobility modes; avoid identity inference |
| Capture/provenance | compression, screenshot UI, watermark, crop lineage, generative/edit artifacts |
| Negative clues | expected but absent features, incompatible road rules, impossible terrain or season |

For every clue, record:

- exact frame location;
- raw visual observation;
- alternative readings or interpretations;
- clue family;
- readability/visibility;
- geographic specificity;
- expected stability over time;
- potential privacy risk;
- next verification action.

### Text extraction protocol

- Inspect the original and multiple targeted crops.
- Try perspective correction, rotation, contrast, sharpening, and channel/grayscale variants when useful.
- Treat OCR output as a set of hypotheses, not a transcription.
- Keep ambiguous characters explicit, for example `NE?`, `N?L`, or `[A/O]`.
- Search alternative readings separately before combining them.
- Never allow a guessed plaque title to override contradictory regional clues.

### Privacy rule for plates and people

Use only the minimum plate information needed for geographic classification, such as country format or regional prefix. Do not publish a complete private vehicle plate. Do not identify a private person by face.

## Stage 3 — Rank clue value

Not every visible feature deserves equal weight. Score each clue from 0–3 on:

- **Readability:** how clearly it is observed;
- **Specificity:** how narrowly it constrains geography, time, or object identity;
- **Stability:** whether it is likely to remain fixed and map-verifiable;
- **Independence:** whether it adds a new signal rather than repeating another clue;
- **Falsifiability:** whether a candidate can clearly pass or fail against it.

Prioritize clues that are clear, distinctive, stable, and independently testable. A partially readable regional plate prefix may be more valuable than a generic royal statue; a precise building façade may be more valuable than vegetation common across a continent.

Do not discard low-confidence clues. Keep them as alternate hypotheses with lower weight.

## Stage 4 — Open parallel search lanes

Search major clue families separately before merging them. This reduces confirmation bias and reveals contradictions early.

Recommended lanes:

1. **Text lane:** exact and alternative transcriptions, translations, names, business fragments.
2. **Object lane:** reverse-image search and descriptive search for distinctive art, monuments, signs, or infrastructure.
3. **Administrative lane:** plate formats, road rules, public signage systems, municipal symbols.
4. **Built-environment lane:** architecture, street furniture, transit infrastructure, business type.
5. **Landscape lane:** terrain, shoreline, vegetation, weather, sun and season.
6. **Provenance lane:** earliest publication, source page, archive captures, related frames.

Use multiple reverse-image engines or visual-search approaches where available. A reverse-image hit must be checked for:

- exact shape and damage/wear patterns;
- plaque placement;
- adjacent buildings and vegetation;
- whether it is the original object or merely the same subject/theme;
- publication lineage and copying.

## Stage 5 — Generate multiple candidates

Maintain at least 2–5 plausible candidates until discriminating evidence eliminates them. Include an “unresolved/other” option.

For each candidate, state:

- why it was generated;
- which clue families support it;
- which clues are unknown;
- what would disprove it fastest;
- the next highest-information verification step.

Do not let the first plausible search result become the de facto answer.

## Stage 6 — Candidate matrix and source-lineage control

Use `templates/location-candidate-matrix.csv`.

Score each candidate against each material clue:

- `+2` exact or highly distinctive match;
- `+1` compatible but non-unique;
- `0` unknown/not testable;
- `-1` tension or weak mismatch;
- `-2` direct contradiction.

Multiply by clue weight when useful. Record the source and reasoning for every non-zero score.

### Independence rules

Do not count these as independent corroboration:

- multiple pages copying the same article or press release;
- directories syndicating one address database;
- reposts of the same photograph;
- two search snippets sourced from one underlying page;
- an article and a summary generated from that article.

Record the likely source lineage. Prefer different evidence mechanisms, for example:

- regional plate convention;
- exact statue photograph;
- official municipal map;
- satellite geometry;
- independent business address tied to a visible storefront.

## Stage 7 — Exact-scene and geometric verification

Once the city or candidate venue is plausible, stop broad searching and reconstruct the camera geometry.

Verify:

- exact object position;
- camera side of the object;
- visible façade sequence and roofline;
- road, path, water, fence, and vegetation order;
- likely camera heading and field of view;
- which street lies **behind**, **across from**, or **adjacent to** the photographer;
- whether addresses refer to the object's mailing address or to the road actually asked for.

Use, as available:

- official maps and cadastral/parcel maps;
- street-level imagery from more than one date;
- satellite/aerial imagery;
- building footprints and address points;
- business directories tied to visible signs;
- photographs from different viewpoints;
- terrain and sun-position tools.

A nearby address is not a geometric proof. A venue may have entrances on multiple streets. A monument can be described as “near Street A” while the street visible behind the camera is Street B.

## Stage 8 — Deliberate falsification

Before finalizing, perform at least two adversarial checks against the leading candidate.

Examples:

- Search for another object with the same name or theme.
- Compare the exact crown, shield, plaque, damage, tree trunk, façade, or skyline silhouette.
- Test whether the plate prefix or road design is incompatible.
- Look at the scene from the opposite side and from older imagery.
- Inspect the second-best candidate using the same rigor.
- Ask what should be visible if the leading candidate were correct, then check whether it is present.

Explicitly document contradictions. Do not silently reinterpret them away.

## Stage 9 — Time verification

When time matters, separate:

- capture time;
- upload/publication time;
- event time;
- archive capture time.

Use shadows, sun position, weather records, vegetation, construction history, signage, schedules, and image provenance as independent signals. Report a range unless multiple signals justify precision.

## Stage 10 — Answer gate

Before submitting, complete this checklist:

- [ ] The exact question and requested granularity are answered.
- [ ] The full frame was inventoried before hypothesis commitment.
- [ ] At least three clue families were considered.
- [ ] City/region is supported by two independent clue families or an exact authoritative source.
- [ ] Exact object/scene identity has been tested against near-matches.
- [ ] The requested street/building/direction is geometrically verified.
- [ ] Source independence has been checked.
- [ ] At least two falsification attempts were performed.
- [ ] Contradictions and alternate candidates are stated.
- [ ] Confidence reflects the weakest necessary link, not the strongest clue.

If the gate is not met, return the best candidates and the unresolved discriminators instead of a precise but fragile answer.

## Reporting format

1. **Answer** and confidence.
2. **Exact target interpretation** — what was identified and from which viewpoint.
3. **Clue inventory summary** — include both supporting and contradictory clues.
4. **Candidate comparison** — why the winner beat the alternatives.
5. **Geometric verification** — map/street/satellite relationship.
6. **Source lineage and independence**.
7. **Limitations and remaining uncertainty**.

Clearly label each statement as verified fact, corroborated inference, single-source lead, contradicted, or unknown.

## Boundaries

- Do not identify a private person by face.
- Do not infer or reveal a private residence or live location.
- Do not publish complete private vehicle plates.
- AI geolocation, OCR, and visual similarity are leads only and require independent confirmation.
