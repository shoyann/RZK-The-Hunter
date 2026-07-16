# Example — Avoiding a Single-Clue Geolocation Failure

## Scenario

A selfie shows a large carved royal figure in a landscaped public area. The task asks for the name of the street behind the photographer.

## Fragile path

1. Read a blurred plaque as the name of a historical king.
2. Search for a wooden sculpture of that king.
3. Find a visually similar sculpture in a botanical garden.
4. Return a street adjacent to that garden.

This path fails because it confuses:

- the same historical subject with the same physical sculpture;
- a venue description with exact camera geometry;
- one plausible source with independent corroboration.

## Multi-signal path

### 1. Inventory the full frame

Potential clues include:

- uncertain plaque text;
- exact crown, beard, shield, trunk and plaque geometry;
- a partial regional registration prefix;
- lakefront-like landscaping;
- a row of red-roofed mixed-use buildings;
- parked-car orientation;
- business signage and street-level awnings;
- the spatial order: photographer → sculpture/green strip → parked cars/road → buildings.

### 2. Search independent lanes

- Plaque/name lane produces multiple cities and remains non-exclusive.
- Registration-system lane points to one region.
- Exact sculpture-image lane identifies a lakeside royal-sculpture group in that region.
- Business/façade lane anchors the background building row to a numbered address range.
- Map and aerial imagery identify the road between the green strip and those buildings.

### 3. Test the near-match

The botanical-garden candidate fails on:

- regional plate compatibility;
- exact sculpture morphology;
- background façade sequence;
- water/urban-layout context;
- the requested camera-to-road relationship.

### 4. Answer only after geometry

The final street is derived from the mapped road lying behind the photographer from the reconstructed viewpoint, not merely from the sculpture's mailing address or a nearby entrance.

## Lesson

For exact geolocation, require agreement among **object identity, regional system clues, built environment, and map geometry**. The weakest necessary link controls confidence.
