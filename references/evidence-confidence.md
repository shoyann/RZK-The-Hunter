# Evidence and Confidence Rubric

## Source classes

- **Primary authoritative:** official registry, court filing, regulator, organization statement, original media, directly observed technical record.
- **Primary non-authoritative:** eyewitness post, user-uploaded media, self-published profile, repository commit.
- **Secondary high quality:** reputable reporting or analysis with transparent sourcing and corrections.
- **Secondary aggregate:** databases, people-search tools, scraped indexes, automated enrichers.
- **Community / anonymous:** forums, reposts, unattributed screenshots, anonymous claims.

## Reliability questions

1. Who produced the source and why?
2. Is the source original or copied?
3. Is the timestamp trustworthy and in which timezone?
4. Can the method be reproduced?
5. Does the source have direct access to the fact?
6. Is there corroboration from an independent source?
7. What evidence would disprove the claim?
8. Could two entities share the same name, username, IP, address, number, date, or image?
9. Is material first-party evidence still unprocessed?
10. Could the apparent corroboration be search coincidence produced by one mistaken pivot?

## Confidence levels

### High

- Supported by an authoritative primary source, or multiple independent reliable sources
- Identity and timing are resolved
- No credible contradictory evidence remains
- Method is reproducible
- Material first-party evidence has been processed or explicitly bounded
- Deliberate falsification did not overturn the claim

### Medium

- Supported by one reliable source plus partial corroboration
- Some assumptions or unresolved identity/timing issues remain
- Alternative explanations are possible but less likely
- Some primary evidence may remain unresolved, but it is not currently known to be decisive

### Low

- Single-source, indirect, stale, scraped, ambiguous, or search-coincidence-dominated evidence
- Material contradictions or gaps remain
- Important first-party evidence is still unprocessed
- Useful as a lead, not a conclusion

## Finding labels

- **Verified fact:** direct, reproducible support
- **Corroborated inference:** reasoned conclusion from multiple facts; state the reasoning
- **Open hypothesis:** coherent explanation that has not yet passed falsification/convergence gates
- **Single-source lead:** plausible but unverified
- **Contradicted:** credible evidence points against the claim
- **Unknown:** insufficient evidence

## Submission-safe is stricter than high confidence

A finding may feel highly likely and still be unsafe to submit as a precise final answer.

Treat an answer as **submission-safe** only when:

- the exact task and output format are understood;
- material first-party evidence is processed or bounded;
- source-signaled alternate representations/transformations are resolved;
- the leading hypothesis has survived at least one deliberate falsification attempt;
- credible contradictions are resolved;
- no unresolved primary artifact could plausibly overturn the answer;
- final wording is derived from the evidence/task format rather than guessed by repeated mutations.

If these conditions are not met, report the best current hypothesis and next discriminator instead of a brittle final answer.

See `references/hypothesis-convergence.md` for the state machine and rejection loop.

## Search-coincidence warning

A dense cluster of matching web results is not automatically strong evidence.

Lower confidence when:

- the candidate originated from one distinctive clue and later searches were shaped around it;
- several pages repeat one underlying source;
- the candidate explains secondary details but not the original artifact;
- a stronger first-party evidence branch remains unresolved;
- the analyst begins changing only answer wording after rejection instead of revisiting the claim.

Search can make a wrong hypothesis look increasingly coherent. Independent evidence mechanisms matter more than the number of matching pages.

## Evidence-table minimum fields

- Finding ID
- Claim
- Label and confidence
- Source URL / file
- Source title and publisher
- Published time and accessed time
- Supporting note or short excerpt
- Independence / provenance note
- Contradictions
- Untested primary evidence
- Fastest falsifier
- Analyst notes

## Visual/geolocation confidence gates

For image and video location claims, confidence is limited by the weakest necessary link:

1. **Observation quality** — was the clue actually visible, or inferred from a noisy crop/OCR guess?
2. **Object identity** — is it the exact object/scene, or merely the same person, theme, product, or architectural style?
3. **Regional consistency** — do plate, language, road, architecture, ecology, and administrative systems agree?
4. **Spatial geometry** — does the map/street/satellite relationship answer the exact directional question?
5. **Source independence** — are corroborating pages genuinely independent or copied from one source?
6. **Contradiction handling** — have strong mismatches been resolved rather than ignored?
7. **Artifact completeness** — were material alternate readings/representations of the original media tested when the source or structure signaled them?

### High confidence — exact geolocation

Normally requires:

- clear observations from several clue families;
- city/region confirmation through two independent mechanisms or an exact authoritative source;
- exact-scene/object verification;
- reproducible geometric alignment for the requested street/building/direction;
- deliberate falsification of the leading candidate;
- no unresolved material contradiction;
- no unresolved first-party visual branch that could plausibly change the answer.

### Medium confidence — probable geolocation

- multiple compatible clues but incomplete exact-object or geometry verification;
- one material ambiguity remains;
- candidate is more likely than alternatives but not submission-safe for a precise street or coordinate.

### Low confidence — location lead

- dominated by one ambiguous text reading, AI guess, reverse-image near-match, nearby address, or copied source lineage;
- useful for further search only.

## Independence is about mechanisms, not page count

Three pages repeating one tourism article count as one lineage. Stronger triangulation combines different mechanisms, for example:

- a plate-system reference;
- an exact photograph of a sculpture;
- an official map;
- satellite geometry;
- a storefront/address record tied to a visible façade.
