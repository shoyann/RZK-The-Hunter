# RZK // THE HUNTER

## Field Intelligence Operations Manual

> **ROZOOKA INDUSTRIES**<br>
> Intelligence Systems Division<br>
> Package designation: `awesome-osint-operator`<br>
> Release: `v1.4.0`<br>
> Handling: Public-source intelligence only

The Hunter is a field-ready OSINT operating system for turning open web research into traceable, defensible intelligence.

This is not a link dump. It is a disciplined workflow for scoping a mission, selecting the right tools, preserving evidence, testing competing hypotheses, and reporting only what the record can support.

## Low-Steering Field Evaluation

The Hunter has been used in near-black-box OSINT challenge runs: the original task was handed directly to the host AI, with operator input typically limited to the task itself and occasional `retry`.

This setup reached **Global #4 on OSINT UK** and **Global #8 on OSINT Industries** within 48 hours. These are field results of `host model + The Hunter + available tools`, not a controlled benchmark.

## Mission Profile

The package is built for researchers, investigators, analysts, journalists, and security teams working with lawful public sources.

It covers:

- domain and infrastructure research
- company and organization mapping
- username and social-account research
- public-interest people research
- purpose-bound private-person profiling from public or authorized sources
- guarded official wanted/fugitive-person location intelligence from public evidence
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
2. Do not bypass authentication, paywalls, rate limits, robots controls, or technical access controls. A CAPTCHA is not an automatic mission failure: try lawful public alternatives first, or pause for a human checkpoint so the operator can complete ordinary verification manually.
3. Collect the minimum personal data necessary for the stated purpose. Bounded private-person profiling is allowed when it is necessary, proportionate, and tied to a legitimate investigation objective.
4. Never obtain, expose, or redistribute credentials, tokens, private keys, raw breach data, or stealer-log contents.
5. Do not support doxxing, stalking, harassment, covert tracking, abusive or invasive dossier building, or biometric identification of private people. The only person-location exception is the guarded official wanted/fugitive workflow, which is limited to bounded inference from public evidence and does not permit continuous live surveillance.
6. Keep threat intelligence defensive: work with hashes, IOCs, reports, sandbox summaries, and vendor analysis.
7. Verify freshness, provenance, identity, timestamps, source independence, and contradictory evidence.
8. For exact geolocation, require clue diversity, geometric verification, and deliberate rejection of near-matches.

Read [`references/safety-policy.md`](references/safety-policy.md) before any guarded investigation involving people, usernames, email, phone, breach exposure, dark-web references, threat actors, or official wanted/fugitive cases.

### Official wanted/fugitive mode

The Hunter includes a dedicated public-safety workflow for **adults who are currently named in an active official wanted/fugitive notice** issued by a recognized government, court, prosecutor, police service, INTERPOL, Europol, or equivalent authority.

Before the mode activates, the agent must verify the official notice, lock the target identity, confirm adult status and lawful purpose, and keep collection inside public, lawfully accessible, or operator-supplied evidence.

Once those gates pass, the workflow may geolocate public media, correlate public timestamps and scene clues, build a location timeline, and report a last-known or recently evidenced location. Exact places or coordinates are allowed only when the evidence supports them and must carry freshness, confidence, contradictions, and an official-status recheck.

This mode does **not** authorize private-account access, credential or breach-data use, device/carrier/brokered telemetry, deception, third-party contact, continuous minute-by-minute surveillance, or tactical apprehension guidance. See [`workflows/wanted-person-location-intelligence.md`](workflows/wanted-person-location-intelligence.md).

### CAPTCHA and human checkpoints

The Hunter treats CAPTCHA as an **access barrier**, not a hard mission stop.

```text
PUBLIC SOURCE
    ↓
CAPTCHA / HUMAN VERIFICATION
    ├── lawful public alternative found → continue
    └── HUMAN CHECKPOINT
              ↓
       operator verifies manually
              ↓
            resume
```

The agent may ask the operator to complete ordinary CAPTCHA verification in the normal browser interface, then continue the investigation in the same authorized session. The agent must not automate CAPTCHA circumvention, use solving farms, or extract/replay CAPTCHA tokens, session cookies, authentication material, or other verification artifacts.

### Purpose-bound private-person profiling

Private-person profiling is **guarded, not categorically forbidden**. The Hunter may build a bounded profile when doing so is necessary to answer a legitimate investigation question and the evidence comes from public or authorized sources.

Typical in-scope elements can include public usernames, public work history, public projects, public statements, account relationships, organizational ties, and relevant timelines. The collection must remain proportionate to the objective.

The Hunter should not drift from a bounded investigation into an invasive life dossier. Unnecessary home addresses, family mapping, personal phone numbers, real-time location, sensitive-trait inference, or unrelated personal details remain restricted or prohibited according to the safety policy.

## Deployment

### v1.4 — Adaptive Investigation Strategy

The Hunter now asks **which feasible action could change the evidence state most
cheaply**, before choosing a tool. It connects pending falsifiers to actual
actions, suggests representation/source-habitat pivots when search repeats,
keeps historical and current evidence separate, and parks unexplained clues
without forcing them into an answer. Safety and convergence gates are unchanged.

- [Strategy doctrine](references/adaptive-investigation-strategy.md)
- [Compact branch checkpoint](templates/strategy-checkpoint.md)
- [Read-only trajectory audit and evaluation protocol](references/trajectory-evaluation.md)

The auditor flags patterns in recorded, annotated actions. It does not browse,
rank people, verify source truth or approve a final answer. Synthetic trace tests
are regression infrastructure, **not measured proof of improved model solve rate**.
No automatic memory retriever or numeric action scheduler is shipped in v1.4.

### Install the complete package

Place the package in your agent's skills directory, or point the agent directly at `SKILL.md`.

Use the release archive or a full checkout: copying only `SKILL.md` (or leaving a
sparse checkout) omits required references and scripts. After an update, verify
the installed copy with `python scripts/verify_package.py`.

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

Optionally audit a recorded case using the documented trace schema:

```bash
python scripts/trajectory_eval.py case/trajectory.json
```

An audit is advisory; see the evaluation protocol before interpreting metrics.

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
| `workflows/` | Mission-specific operating procedures, including the guarded official wanted/fugitive workflow |
| `templates/` | Investigation plans, evidence ledgers, clue inventories, matrices, and report formats |
| `scripts/` | Catalog search, workflow selection, evidence tracking, visual cases, synchronization, and verification |
| `tests/` | Package/catalog tests, synthetic trace regressions, and raw behavioral evaluation packets |

## Provenance

This package is an adaptation of [`jivoi/awesome-osint`](https://github.com/jivoi/awesome-osint). The upstream source snapshot is distributed under **CC BY-SA 4.0**. Preserve [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`LICENSE.txt`](LICENSE.txt) when redistributing or adapting the package.

Catalog snapshot timestamp: `2026-07-13T08:03:02+00:00`<br>
Snapshot SHA-256: `5071f31d2e0fda75368b9021091b77d74a6824895ca953b5bc1cc109401a474b`

---

**RZK // ROZOOKA INDUSTRIES**<br>
Signal over spectacle. Evidence over instinct.
