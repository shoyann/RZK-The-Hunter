<div align="center">

<img src="assets/the-hunter-icon.png" alt="The Hunter icon" width="220">

# RZK // THE HUNTER

**A parasitic investigation skill for AI agents.**  
Adaptive research · verified sources · traceable evidence

![Release](https://img.shields.io/badge/release-v1.4.0-A23B46?style=flat-square&labelColor=2B2F33)
![Discipline](https://img.shields.io/badge/discipline-OSINT-2F6F7E?style=flat-square&labelColor=2B2F33)
![Handling](https://img.shields.io/badge/handling-public_sources_only-A4772B?style=flat-square&labelColor=2B2F33)
![Runtime](https://img.shields.io/badge/runtime-agent_native-5D7048?style=flat-square&labelColor=2B2F33)

[Overview](#overview) · [Field results](#field-results) · [Quick start](#quick-start) · [Field kit](#field-kit) · [Doctrine](#operating-doctrine) · [Package map](#package-map)

</div>

> [!IMPORTANT]
> **The Hunter is an operating system for disciplined open-source investigation—not a link dump.** It scopes the mission, selects the next useful action, preserves evidence, tests competing hypotheses, and reports only what the record can support.

| Designation | Release | Division | Handling |
| --- | --- | --- | --- |
| `awesome-osint-operator` | Release: `v1.4.0` | Rozooka Industries / Intelligence Systems | Public-source intelligence only |

## Overview

The Hunter turns open-web research into traceable, defensible intelligence. It is built for researchers, investigators, analysts, journalists, and security teams working with lawful public sources.

Its core loop is simple:

1. Define the question, scope, authorization, and stop condition.
2. Choose the feasible action most likely to change the evidence state.
3. Capture sources and separate verified fact from inference.
4. Challenge the leading hypothesis with contradictions and near-matches.
5. Stop when the evidence threshold is met—or state exactly what remains unknown.

## Field results

The Hunter has been used in near-black-box OSINT challenge runs: the original task was handed directly to the host AI, with operator input typically limited to the task itself and occasional `retry`.

| Evaluation | Result | Window | Steering |
| --- | ---: | --- | --- |
| OSINT UK | **Global #4** | Within 48 hours | Low |
| OSINT Industries | **Global #8** | Within 48 hours | Low |

> [!NOTE]
> These are field results of `host model + The Hunter + available tools`, not a controlled benchmark or a claim that the skill alone produced the ranking.

## Mission profile

| Investigation surface | Supported work |
| --- | --- |
| Infrastructure | Domains, DNS, certificates, hosting, and technical relationships |
| Organizations | Companies, ownership, filings, and organizational mapping |
| Identities | Usernames, public accounts, public-interest people, and purpose-bound private-person research |
| Visual evidence | Image/video provenance, geolocation, scene comparison, and timestamp verification |
| Claims and events | News verification, source triangulation, timelines, and contradiction tracking |
| Defensive intelligence | Email/phone exposure checks, IOCs, threat reports, and monitoring plans |
| Guarded public safety | Supports guarded official wanted/fugitive-person location intelligence from bounded public evidence |

## Quick start

Install the **complete package** in the host agent's skills directory, or point the agent directly at [`SKILL.md`](SKILL.md).

```text
awesome-osint-operator/
├── SKILL.md
├── references/
├── scripts/
├── templates/
├── tests/
└── workflows/
```

Use a release archive or a full checkout. Copying only `SKILL.md`—or using a sparse checkout—omits required references and scripts.

After installation or an update, verify the package:

```bash
python scripts/verify_package.py
```

The primary operating instructions live in [`SKILL.md`](SKILL.md). The remaining directories provide the catalog, playbooks, evidence tools, templates, and validation suite.

## What's new in v1.4

### Adaptive Investigation Strategy

The Hunter now asks **which feasible action could change the evidence state most cheaply** before choosing a tool.

- Connects pending falsifiers to concrete actions.
- Suggests representation and source-habitat pivots when search begins to repeat.
- Keeps historical and current evidence separate.
- Parks unexplained clues instead of forcing them into an answer.
- Preserves the existing safety and convergence gates.

Read the supporting material:

- [Strategy doctrine](references/adaptive-investigation-strategy.md)
- [Compact branch checkpoint](templates/strategy-checkpoint.md)
- [Read-only trajectory audit and evaluation protocol](references/trajectory-evaluation.md)

The auditor flags patterns in recorded, annotated actions. It does not browse, rank people, verify source truth, or approve a final answer. Synthetic trace tests are regression infrastructure, **not measured proof of improved model solve rate**. No automatic memory retriever or numeric action scheduler is shipped in v1.4.

## Field kit

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

### Audit and verify

Optionally audit a recorded case using the documented trace schema:

```bash
python scripts/trajectory_eval.py case/trajectory.json
```

An audit is advisory; read the evaluation protocol before interpreting its metrics.

```bash
python scripts/sync_catalog.py
python scripts/verify_package.py
python -m unittest discover -s tests -v
```

## Operating doctrine

Every operation begins with a scope and a stop condition. Every material claim is tied to a source. Every conclusion is separated into fact, inference, and unknown.

1. Use public and lawfully accessible sources only.
2. Do not bypass authentication, paywalls, rate limits, robots controls, or technical access controls. A CAPTCHA is not an automatic mission failure: try lawful public alternatives first, or pause for a human checkpoint so the operator can complete ordinary verification manually.
3. Collect the minimum personal data necessary for the stated purpose. Bounded private-person profiling is allowed only when it is necessary, proportionate, and tied to a legitimate investigation objective.
4. Never obtain, expose, or redistribute credentials, tokens, private keys, raw breach data, or stealer-log contents.
5. Do not support doxxing, stalking, harassment, covert tracking, abusive or invasive dossier building, or biometric identification of private people. The only person-location exception is the guarded official wanted/fugitive workflow, limited to bounded inference from public evidence; it does not permit continuous live surveillance.
6. Keep threat intelligence defensive: work with hashes, IOCs, reports, sandbox summaries, and vendor analysis.
7. Verify freshness, provenance, identity, timestamps, source independence, and contradictory evidence.
8. For exact geolocation, require clue diversity, geometric verification, and deliberate rejection of near-matches.

Read [`references/safety-policy.md`](references/safety-policy.md) before any guarded investigation involving people, usernames, email, phone, breach exposure, dark-web references, threat actors, or official wanted/fugitive cases.

<details>
<summary><strong>Official wanted/fugitive mode</strong></summary>

The Hunter includes a dedicated public-safety workflow for **adults who are currently named in an active official wanted/fugitive notice** issued by a recognized government, court, prosecutor, police service, INTERPOL, Europol, or equivalent authority.

Before the mode activates, the agent must verify the official notice, lock the target identity, confirm adult status and lawful purpose, and keep collection inside public, lawfully accessible, or operator-supplied evidence.

Once those gates pass, the workflow may geolocate public media, correlate public timestamps and scene clues, build a location timeline, and report a last-known or recently evidenced location. Exact places or coordinates are allowed only when the evidence supports them and must carry freshness, confidence, contradictions, and an official-status recheck.

This mode does **not** authorize private-account access, credential or breach-data use, device/carrier/brokered telemetry, deception, third-party contact, continuous minute-by-minute surveillance, or tactical apprehension guidance. See [`workflows/wanted-person-location-intelligence.md`](workflows/wanted-person-location-intelligence.md).

</details>

<details>
<summary><strong>CAPTCHA and human checkpoints</strong></summary>

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

</details>

<details>
<summary><strong>Purpose-bound private-person profiling</strong></summary>

Private-person profiling is **guarded, not categorically forbidden**. The Hunter may build a bounded profile when doing so is necessary to answer a legitimate investigation question and the evidence comes from public or authorized sources.

Typical in-scope elements can include public usernames, public work history, public projects, public statements, account relationships, organizational ties, and relevant timelines. Collection must remain proportionate to the objective.

The Hunter must not drift from a bounded investigation into an invasive life dossier. Unnecessary home addresses, family mapping, personal phone numbers, real-time location, sensitive-trait inference, or unrelated personal details remain restricted or prohibited under the safety policy.

</details>

## Reporting standard

Use this structure for an operational report:

1. Executive summary
2. Scope, authorization, and limitations
3. Key findings with confidence
4. Evidence table
5. Timeline or relationship map, when useful
6. Contradictions and unresolved questions
7. Methods and tools used
8. Privacy and handling notes
9. Sources

Use precise conclusion labels:

| Label | Meaning |
| --- | --- |
| **Verified fact** | Directly supported by an authoritative source |
| **Corroborated inference** | Supported by multiple independent signals |
| **Single-source lead** | Useful direction, not a conclusion |
| **Unresolved / unknown** | The record is insufficient |

## Package map

| Asset | Role |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Core operating doctrine and execution rules |
| `references/catalog.json` / `references/catalog.csv` | Structured tool catalog |
| `references/` | Safety policy, confidence rubric, taxonomy, query playbook, and source snapshot |
| `workflows/` | Mission-specific procedures, including the guarded official wanted/fugitive workflow |
| `templates/` | Investigation plans, evidence ledgers, clue inventories, matrices, and report formats |
| `scripts/` | Catalog search, workflow selection, evidence tracking, visual cases, synchronization, and verification |
| `tests/` | Package/catalog tests, synthetic trace regressions, and raw behavioral evaluation packets |

## Provenance and licensing

This package is an adaptation of [`jivoi/awesome-osint`](https://github.com/jivoi/awesome-osint). The upstream source snapshot is distributed under **CC BY-SA 4.0**. Preserve [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`LICENSE.txt`](LICENSE.txt) when redistributing or adapting the package.

Catalog snapshot timestamp: `2026-07-13T08:03:02+00:00`  
Snapshot SHA-256: `5071f31d2e0fda75368b9021091b77d74a6824895ca953b5bc1cc109401a474b`

---

<div align="center">

**RZK // ROZOOKA INDUSTRIES**  
Signal over spectacle. Evidence over instinct.

</div>
