# RZK // THE HUNTER

## Field Intelligence Operations Manual

> **ROZOOKA INDUSTRIES**<br>
> Intelligence Systems Division<br>
> Package designation: `awesome-osint-operator`<br>
> Release: `v1.1.0`<br>
> Handling: Public-source intelligence only

The Hunter is a field-ready OSINT operating system for turning open web research into traceable, defensible intelligence.

This is not a link dump. It is a disciplined workflow for scoping a mission, selecting the right tools, preserving evidence, testing competing hypotheses, and reporting only what the record can support.

## Mission Profile

The package is built for researchers, investigators, analysts, journalists, and security teams working with lawful public sources.

It covers:

- domain and infrastructure research
- company and organization mapping
- username and social-account research
- public-interest people research
- defensive email and phone exposure checks
- image and video provenance
- geolocation and scene verification
- news and claim verification
- defensive threat intelligence
- monitoring plans and escalation rules

## Operating Doctrine

Every operation begins with a scope and a stop condition. Every material claim is tied to a source. Every conclusion is separated into fact, inference, and unknown.

The Hunter follows these rules:

1. Use public and lawfully accessible sources only.
2. Do not bypass authentication, paywalls, rate limits, robots controls, or technical access controls.
3. Collect the minimum personal data necessary for the stated purpose.
4. Never obtain, expose, or redistribute credentials, tokens, private keys, raw breach data, or stealer-log contents.
5. Do not support doxxing, stalking, harassment, covert tracking, invasive profiling, or biometric identification of private people.
6. Keep threat intelligence defensive: work with hashes, IOCs, reports, sandbox summaries, and vendor analysis.
7. Verify freshness, provenance, identity, timestamps, source independence, and contradictory evidence.
8. For exact geolocation, require clue diversity, geometric verification, and deliberate rejection of near-matches.

Read [`references/safety-policy.md`](references/safety-policy.md) before any guarded investigation involving people, usernames, email, phone, breach exposure, dark-web references, or threat actors.

## Deployment

Place the package in your agent's skills directory, or point the agent directly at `SKILL.md`.

```text
awesome-osint-operator/
├── SKILL.md
├── references/
├── scripts/
├── templates/
├── tests/
└── workflows/
```

The primary operating instructions live in [`SKILL.md`](SKILL.md). The rest of the package provides the catalog, playbooks, evidence tools, templates, and validation suite.

## Field Kit

### Search the catalog

```bash
python scripts/search_catalog.py "domain DNS certificates history" --top 10
python scripts/search_catalog.py "company ownership public filings" --top 10
```

### Select tools by workflow

```bash
python scripts/select_tools.py --workflow domain --per-stage 2
python scripts/select_tools.py --workflow image --per-stage 2
```

### Open an evidence ledger

```bash
python scripts/evidence_ledger.py init case/evidence.csv
python scripts/evidence_ledger.py add case/evidence.csv \
  --claim "Example claim" \
  --source-url "https://example.org/source" \
  --source-title "Source title" \
  --source-type primary \
  --confidence medium \
  --notes "What the source supports and what it does not"
```

### Start a visual case

```bash
python scripts/visual_case.py init case/image-001
python scripts/visual_case.py score case/image-001/location-candidates.csv
```

### Maintain and verify the package

```bash
python scripts/sync_catalog.py
python scripts/verify_package.py
python -m unittest discover -s tests -v
```

## Standard Reporting Format

Use the following structure for an operational report:

1. Executive summary
2. Scope, authorization, and limitations
3. Key findings with confidence
4. Evidence table
5. Timeline or relationship map, when useful
6. Contradictions and unresolved questions
7. Methods and tools used
8. Privacy and handling notes
9. Sources

Label conclusions precisely:

- **Verified fact** — directly supported by an authoritative source.
- **Corroborated inference** — supported by multiple independent signals.
- **Single-source lead** — useful direction, not a conclusion.
- **Unresolved / unknown** — the record is insufficient.

## Package Layout

| Asset | Role |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Core operating doctrine and execution rules |
| `references/catalog.json` / `catalog.csv` | Structured tool catalog |
| `references/` | Safety policy, confidence rubric, taxonomy, query playbook, and source snapshot |
| `workflows/` | Mission-specific operating procedures |
| `templates/` | Investigation plans, evidence ledgers, clue inventories, matrices, and report formats |
| `scripts/` | Catalog search, workflow selection, evidence tracking, visual cases, synchronization, and verification |
| `tests/` | Package integrity and catalog tests |

## Provenance

This package is an adaptation of [`jivoi/awesome-osint`](https://github.com/jivoi/awesome-osint). The upstream source snapshot is distributed under **CC BY-SA 4.0**. Preserve [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`LICENSE.txt`](LICENSE.txt) when redistributing or adapting the package.

Catalog snapshot timestamp: `2026-07-13T08:03:02+00:00`<br>
Snapshot SHA-256: `5071f31d2e0fda75368b9021091b77d74a6824895ca953b5bc1cc109401a474b`

---

**RZK // ROZOOKA INDUSTRIES**<br>
Signal over spectacle. Evidence over instinct.
