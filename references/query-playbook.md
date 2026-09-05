# Query Playbook

Use search operators to reduce noise, not to hunt exposed secrets.

At a stall, group attempts by objective, representation, habitat and underlying
source lineage. Rewording with unchanged results is not evidence progress.
Consider [representation/habitat pivots or method search](adaptive-investigation-strategy.md)
before another equivalent query. A discovered method is a capability lead, not
evidence or authorization to install tools, upload artifacts or bypass access.

## Core operators

- Exact phrase: `"project name"`
- Site: `site:example.org "annual report"`
- File type: `filetype:pdf "company name"`
- Title / URL: `intitle:"press release"`, `inurl:reports`
- Exclude: `-jobs -careers -pinterest`
- Date bounds where supported: `after:2025-01-01 before:2026-01-01`
- Alternatives: `(alias1 OR alias2 OR "legal name")`

## Entity expansion

For each target, generate:

- Exact legal name and historical names
- Common abbreviations and transliterations
- Official domains and country-code domains
- Key people and roles, only where relevant
- Product, project, subsidiary, or brand names
- Dates, locations, registration numbers, ASNs, hashes, or handles

## Safe recipes

### Company

```text
"Legal Company Name" (annual report OR filing OR registration)
site:official-registry.example "registration number"
"Company Name" (acquisition OR lawsuit OR regulator OR sanction)
```

### Domain

```text
"example.com" (RDAP OR WHOIS OR DNS OR certificate)
site:crt.sh "example.com"
"example.com" (phishing OR malware OR abuse) -site:example.com
```

### News claim

```text
"distinctive claim phrase"
"person or organization" "event" after:YYYY-MM-DD
site:official-source.example "event keyword"
```

### Document discovery

```text
site:example.org filetype:pdf "unique phrase"
"document title" (pdf OR doc OR slides)
```

### Image provenance

Search visible text, signage, landmarks, product labels, weather, event name, and suspected location separately. Reverse-image search should be followed by earliest-source tracing and archive checks.

## Avoid

Do not construct queries designed to find passwords, tokens, `.env` files, private keys, credential dumps, private data, or access panels. For authorized secret-scanning of owned code, use approved defensive tooling and report remediation without exposing secrets.

## Multi-signal image/geolocation recipes

Search clues in separate lanes before combining them.

### Ambiguous text

```text
"exact rare substring"
("reading A" OR "reading B") (statue OR plaque OR monument)
"partial business fragment" city
```

Keep alternate OCR readings separate. Do not silently normalize uncertain characters.

### Exact object rather than shared subject

```text
"historical figure" wooden sculpture crown shield plaque
"object description" city promenade
"distinctive damage or feature" sculpture
```

Compare physical morphology, plaque position, wear, base, landscaping, and background—not merely the depicted figure or theme.

### Regional systems

```text
"plate prefix" registration region
"road sign design" country
"municipal logo description" city
```

Prefer official or authoritative references for administrative codes.

### Background anchor

```text
"visible business fragment" address
"business category" "suspected street"
"building name" satellite map
```

Use businesses to anchor a façade sequence, then verify the road geometrically.

### Candidate falsification

```text
"candidate object name" other city
"candidate venue" opposite entrance map
"candidate street" satellite buildings
```

Search explicitly for duplicates, alternate entrances, and incompatible viewpoints.

### Geometry questions

Translate the user’s wording into map relationships:

```text
object coordinates + camera side + road between object and building row
venue entrances on multiple streets
street behind sculpture viewed toward façade
```

A mailing address is not a substitute for camera geometry.
