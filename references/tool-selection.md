# Tool Selection Matrix

The catalog is large by design. Use this matrix to choose a small, diverse set.

| Objective | Start with | Add for verification | Avoid as primary evidence |
|---|---|---|---|
| Domain / infrastructure | RDAP/WHOIS, DNS, certificate transparency | ASN/BGP, archives, technology fingerprint, reputation | Anonymous scanners, stale scraped summaries |
| Company / organization | Official registry, regulator, filings, company site | Archives, reputable news, ownership datasets | People-search aggregators, unsourced company profiles |
| Username / social | Platform-native search, username checkers | Web search, archives, profile-content consistency | Treating username match alone as identity proof |
| Public-person research | Official biographies, filings, public statements | Reputable reporting, archives, professional records | Home-address/family aggregators, unrelated private data |
| Email / phone defensive check | Ownership confirmation, reputable exposure notification, domain records | Reputation and validation services | Raw leaks, account enumeration without authorization |
| Image / video | Original-file metadata, full-frame clue inventory, targeted crops, reverse image/keyframes | Plate/sign references, exact-object matching, maps, street imagery, satellite, business/address anchors, weather/shadows, archives | AI/OCR as sole evidence, one visually similar object, nearby address without geometry |
| News / claim verification | Original statement and primary records | Independent reporting, archives, media provenance | Reposts, screenshots without source, virality metrics |
| Threat intelligence | Vendor advisories, official CERTs, IOC enrichers | Multiple CTI platforms, passive DNS, reports | Executing samples, operational intrusion, raw criminal data |
| Monitoring | RSS, official feeds, page-change detection | News/search alerts, deduplication, archive snapshots | High-frequency invasive tracking of individuals |

## Selection scorecard

Score each candidate 0–2:

- Direct relevance
- Authority / provenance
- Freshness
- Geographic coverage
- Reproducibility
- Privacy / legal fit
- Independent-source value
- Availability and operational safety

Prefer tools with the highest total, but never let convenience override authority or safety.

## Catalog caveat

Descriptions, free/paid status, and availability in the source list may be stale or promotional. Verify on the current official site before use. Inclusion is not endorsement.


## Image/geolocation selection rule

Choose tools across different **evidence mechanisms**, not merely different websites. A balanced exact-location set normally includes:

- one original-media/metadata method;
- one text or administrative-system method;
- one exact-object or reverse-image method;
- one map/street/satellite geometry method;
- one provenance/archive method when publication history matters.

Do not count multiple wrappers around the same map, database, or image index as independent tools.
