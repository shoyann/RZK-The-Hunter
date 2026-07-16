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
8. Could two entities share the same name, username, IP, address, or image?

## Confidence levels

### High

- Supported by an authoritative primary source, or multiple independent reliable sources
- Identity and timing are resolved
- No credible contradictory evidence remains
- Method is reproducible

### Medium

- Supported by one reliable source plus partial corroboration
- Some assumptions or unresolved identity/timing issues remain
- Alternative explanations are possible but less likely

### Low

- Single-source, indirect, stale, scraped, or ambiguous evidence
- Material contradictions or gaps remain
- Useful as a lead, not a conclusion

## Finding labels

- **Verified fact:** direct, reproducible support
- **Corroborated inference:** reasoned conclusion from multiple facts; state the reasoning
- **Single-source lead:** plausible but unverified
- **Contradicted:** credible evidence points against the claim
- **Unknown:** insufficient evidence

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
- Analyst notes

## Visual/geolocation confidence gates

For image and video location claims, confidence is limited by the weakest necessary link:

1. **Observation quality** — was the clue actually visible, or inferred from a noisy crop/OCR guess?
2. **Object identity** — is it the exact object/scene, or merely the same person, theme, product, or architectural style?
3. **Regional consistency** — do plate, language, road, architecture, ecology, and administrative systems agree?
4. **Spatial geometry** — does the map/street/satellite relationship answer the exact directional question?
5. **Source independence** — are corroborating pages genuinely independent or copied from one source?
6. **Contradiction handling** — have strong mismatches been resolved rather than ignored?

### High confidence — exact geolocation

Normally requires:

- clear observations from several clue families;
- city/region confirmation through two independent mechanisms or an exact authoritative source;
- exact-scene/object verification;
- reproducible geometric alignment for the requested street/building/direction;
- deliberate falsification of the leading candidate;
- no unresolved material contradiction.

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
