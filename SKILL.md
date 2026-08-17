---
name: awesome-osint-operator
description: Ethical, evidence-first OSINT planning, tool selection, verification, monitoring, and reporting using a structured catalog adapted from jivoi/awesome-osint. Use for public-source domain, company, username, image, geospatial, news, fact-checking, and defensive threat-intelligence research. Do not use for doxxing, stalking, credential acquisition, access bypass, real-time tracking, or abusive/invasive profiling.
license: CC-BY-SA-4.0
version: 1.1.1
---

# Awesome OSINT Operator

Turn a giant tool list into a disciplined investigation workflow. The catalog is a **lead generator**, not evidence. A tool result is never a finding until it is independently verified and cited.

## Non-negotiable operating rules

1. **Scope first.** Record the target, legitimate purpose, jurisdiction, time range, allowed sources, and prohibited actions.
2. **Use public and lawfully accessible sources only.** Do not bypass authentication, paywalls, rate limits, robots controls, or technical access controls. A CAPTCHA is an access barrier, not an automatic mission stop: do not automate its circumvention. First try lawful public alternatives; when ordinary user verification is available, pause and request a human checkpoint so the operator can complete the challenge manually in the normal browser, then resume. Never extract, export, replay, or transfer CAPTCHA tokens, session cookies, or authentication material.
3. **Minimize personal data.** Purpose-bound profiling of private individuals is permitted when it is necessary to a legitimate investigation, proportionate to the objective, and limited to public or authorized sources. Avoid unnecessary or invasive profiling, sensitive-trait inference, minors, home addresses, family mapping, real-time location, and unrelated personal details.
4. **Never obtain or expose credentials.** Breach-related tools may be used only for defensive exposure checks on assets the user owns or is authorized to assess. Report exposure status and remediation, never passwords, tokens, raw dumps, or stealer-log contents.
5. **No doxxing, stalking, harassment, or biometric identification.** Reverse-image provenance and scene verification are acceptable; identifying a private person by face is not.
6. **Threat intelligence stays defensive.** Prefer hashes, IOCs, reports, sandbox summaries, and vendor analysis. Do not execute malware or download samples unless the user has explicit authorization and a dedicated safe environment.
7. **Verify freshness.** Tools and facts change. Check current availability, terms, and dates before relying on a catalog entry.
8. **Cite every material claim.** Preserve source URL, title, publisher, publication date, access time, and a short supporting excerpt or note.
9. **Separate fact, inference, and unknown.** State confidence and contradictions explicitly.
10. **Do not dump hundreds of links.** Select the smallest useful set—normally 3–7 tools—explain why each is chosen, and include a fallback.
11. **For images and video, inventory before searching.** Sweep the entire frame, record alternate readings, keep multiple candidates alive, and require independent clue families plus geometric verification before a precise location answer.

Read `references/safety-policy.md` before any people, username, email, phone, breach, dark-web, or threat-actor task.

## Default workflow

### 1. Intake and safety gate

Capture:
- Objective and decision the research will support
- Target type and known identifiers
- Time window and geography
- Authorization / public-interest basis
- Sensitive-data risks
- Stop conditions

Classify the request:
- **Low risk:** company, domain ownership, public filings, official statements, news verification, image provenance, public infrastructure, academic research.
- **Guarded:** usernames, public-person research, purpose-bound private-person profiling, email/phone exposure checks, breach status, social graphing, threat actors, dark-web references.
- **Disallowed:** credentials, doxxing, stalking, covert tracking, private-account access, deanonymization for harassment, abusive or invasive dossier building, targeted surveillance of vulnerable people, or illegal access.

For guarded work, narrow scope, prefer first-party or official sources, and redact unnecessary PII.

### 2. Build a collection plan

Choose the matching workflow:
- `workflows/domain-infrastructure.md`
- `workflows/company-org.md`
- `workflows/username-social.md`
- `workflows/people-public-interest.md`
- `workflows/email-phone-defensive.md`
- `workflows/image-video-geolocation.md`
- `workflows/news-fact-check.md`
- `workflows/threat-intelligence.md`
- `workflows/monitoring.md`

Start from hypotheses and questions, not tools. Define what evidence would confirm or falsify each hypothesis.

For image/video tasks, first read `references/visual-clue-taxonomy.md` and create a clue inventory from `templates/visual-clue-inventory.csv`. Do not let the first readable sign, plaque, face, logo, or reverse-image hit become the answer.

### 3. Select tools from the catalog

Search locally:

```bash
python scripts/search_catalog.py "reverse image metadata geolocation" --top 12
python scripts/search_catalog.py "域名 DNS 证书历史" --top 12
python scripts/select_tools.py --workflow domain --per-stage 2
python scripts/visual_case.py init case/image-001
```

Defaults exclude `restricted` entries. Treat catalog cost/auth signals as hints only; verify them on the tool's current official page.

Selection criteria:
- Direct relevance to the question
- Source authority and transparency
- Freshness and geographic coverage
- Privacy and legal fit
- Reproducibility
- Independent-source diversity
- Lowest necessary risk

### 4. Collect broad-to-narrow

For visual investigations, collect **frame-wide clues before web results**: full-frame scene model, grid/semantic crops, uncertain transcriptions, clue-family scoring, and at least two competing candidates.

Use this source order unless the workflow says otherwise:
1. Official / first-party sources
2. Primary records and registries
3. Reputable archives and datasets
4. Search engines and discovery tools
5. Secondary reporting and aggregators
6. Community or user-generated sources, clearly labeled

Pivot only on corroborated identifiers. Keep a pivot log so aliases, dates, domains, hashes, and locations do not become mixed across entities.

When a public-source collection route hits a CAPTCHA, classify it as an access barrier. Try lawful alternate public routes first. If the site presents ordinary human verification, pause for an operator checkpoint and resume only after the operator completes the challenge manually. Do not automate CAPTCHA solving or transfer verification/session material between environments.

### 5. Verify and triangulate

A high-confidence claim usually requires either:
- One authoritative primary source, or
- Two genuinely independent reliable sources

Check:
- Whether the exact question is being answered (for example, object location versus street behind the camera)
- Identity consistency
- Timestamp and timezone
- Original publication versus repost
- Archive capture date versus content date
- Image/video provenance and earliest known appearance
- Whether sources copied one another
- Alternative explanations and contradictory evidence
- Source-lineage independence: copied pages and reposted images count as one source
- For exact geolocation, camera/object/road geometry and a deliberate near-match rejection

Use `references/evidence-confidence.md` for the scoring rubric.

### 6. Preserve evidence

Initialize a ledger:

```bash
python scripts/evidence_ledger.py init case/evidence.csv
python scripts/evidence_ledger.py add case/evidence.csv \
  --claim "Example claim" \
  --source-url "https://example.org/source" \
  --source-title "Source title" \
  --source-type primary \
  --confidence medium \
  --notes "What this source supports and what it does not"
```

For local files, record hashes. Do not store unnecessary sensitive data.

### 7. Report

Use this structure:
1. Executive summary
2. Scope, authorization, and limitations
3. Key findings with confidence
4. Evidence table
5. Timeline or relationship map when useful
6. Contradictions and unresolved questions
7. Methods and tools used
8. Privacy / handling notes
9. Sources

Clearly label:
- **Verified fact**
- **Corroborated inference**
- **Single-source lead**
- **Unresolved / unknown**

Use the user's language. Avoid dramatic wording; precision beats certainty theater.

## Operating modes

### Quick tool selection
Return 3–7 tools, grouped by investigation stage. For each: purpose, why it fits, risk/registration caveat, and fallback.

### Investigation plan
Return hypotheses, collection stages, source priorities, verification tests, stop conditions, and deliverables. Do not pretend collection has already happened.

### Full investigation
Perform the plan, keep an evidence ledger, cite all material claims, and publish a confidence-rated report.

### Verification / fact-check
Trace the claim to its earliest available source, validate media provenance, compare independent reporting, identify missing context, and state a verdict with confidence.

### Monitoring
Define entities, keywords, negative keywords, feeds, cadence, alert threshold, deduplication, and escalation criteria. Do not monitor private individuals invasively.

## Catalog maintenance

The included snapshot is from `jivoi/awesome-osint`. Refresh it when internet access is available:

```bash
python scripts/sync_catalog.py
python scripts/verify_package.py
```

The source list is licensed CC BY-SA 4.0. Preserve `ATTRIBUTION.md` and `LICENSE.txt` when redistributing adaptations.

## Progressive references

- Tool catalog: `references/catalog.json`, `references/catalog.csv`
- Source snapshot: `references/source/awesome-osint-README.md`
- Tool-selection matrix: `references/tool-selection.md`
- Query recipes: `references/query-playbook.md`
- Safety rules: `references/safety-policy.md`
- Evidence confidence: `references/evidence-confidence.md`
- Visual clue taxonomy: `references/visual-clue-taxonomy.md`
- Image/video workflow: `workflows/image-video-geolocation.md`
- Visual clue ledger: `templates/visual-clue-inventory.csv`
- Candidate scoring matrix: `templates/location-candidate-matrix.csv`
- Image geolocation report: `templates/image-geolocation-report.md`
- Other report templates: `templates/`
