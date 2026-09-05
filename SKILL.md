---
name: awesome-osint-operator
description: Ethical, evidence-first OSINT planning, tool selection, verification, monitoring, reporting, and guarded official wanted/fugitive-person location intelligence using a structured catalog adapted from jivoi/awesome-osint. Use for public-source domain, company, username, image, geospatial, news, fact-checking, defensive threat-intelligence, and verified official wanted-person research. Do not use for doxxing, stalking, credential acquisition, access bypass, continuous real-time tracking, or abusive/invasive profiling.
license: CC-BY-SA-4.0
metadata:
  version: 1.4.0
---

# Awesome OSINT Operator

Turn a giant tool list into a disciplined investigation workflow. The catalog is a **lead generator**, not evidence. A tool result is never a finding until it is independently verified and cited.

## Non-negotiable operating rules

1. **Scope first.** Record the target, legitimate purpose, jurisdiction, time range, allowed sources, and prohibited actions.
2. **Use public and lawfully accessible sources only.** Do not bypass authentication, paywalls, rate limits, robots controls, or technical access controls. A CAPTCHA is an access barrier, not an automatic mission stop: do not automate its circumvention. First try lawful public alternatives; when ordinary user verification is available, pause and request a human checkpoint so the operator can complete the challenge manually in the normal browser, then resume. Never extract, export, replay, or transfer CAPTCHA tokens, session cookies, or authentication material.
3. **Minimize personal data.** Purpose-bound profiling of private individuals is permitted when it is necessary to a legitimate investigation, proportionate to the objective, and limited to public or authorized sources. Avoid unnecessary or invasive profiling, sensitive-trait inference, minors, home addresses, family mapping, real-time location, and unrelated personal details. A narrower exception exists only for adults who pass the active official wanted/fugitive-person gate in `workflows/wanted-person-location-intelligence.md`.
4. **Never obtain or expose credentials.** Breach-related tools may be used only for defensive exposure checks on assets the user owns or is authorized to assess. Report exposure status and remediation, never passwords, tokens, raw dumps, or stealer-log contents.
5. **No doxxing, stalking, harassment, or biometric identification.** Reverse-image provenance and scene verification are acceptable; identifying a private person by face is not. Bounded public-source location inference is allowed only under the verified official wanted/fugitive-person workflow and never extends to continuous live surveillance.
6. **Threat intelligence stays defensive.** Prefer hashes, IOCs, reports, sandbox summaries, and vendor analysis. Do not execute malware or download samples unless the user has explicit authorization and a dedicated safe environment.
7. **Verify freshness.** Tools and facts change. Check current availability, terms, and dates before relying on a catalog entry.
8. **Cite every material claim.** Preserve source URL, title, publisher, publication date, access time, and a short supporting excerpt or note.
9. **Separate fact, inference, hypothesis, and unknown.** State confidence, contradictions, and what remains untested explicitly.
10. **Do not dump hundreds of links.** Select the smallest useful set—normally 3–7 tools—explain why each is chosen, and include a fallback.
11. **For images and video, inventory before searching.** Sweep the entire frame, record alternate readings, keep multiple candidates alive, and require independent clue families plus geometric verification before a precise location answer.
12. **Do not finalize while material first-party evidence remains unprocessed.** Original files, explicit source hints, embedded resources, metadata, source code, alternate views, and relevant low-risk transformations must be resolved or deliberately ruled out before a lead becomes submission-safe.
13. **A rejected answer is evidence.** Do not keep mutating wording around the same unsupported hypothesis. Roll back to the last verified checkpoint, mark the failed hypothesis, reopen unresolved evidence, change one assumption at a time, and continue the loop.

Read `references/safety-policy.md` before any people, username, email, phone, breach, dark-web, threat-actor, or official wanted/fugitive task.
Read `references/hypothesis-convergence.md` before any multi-stage investigation, puzzle-like artifact chain, or task where a plausible early answer could be overturned by later evidence.
At a consequential branch decision or strategic stall, read `references/adaptive-investigation-strategy.md`. Use it to choose the next evidence-changing action; it adds no collection permissions and does not replace the convergence gate.
For an adult who is currently named in an active official wanted/fugitive notice, verify that status and identity first, then read `workflows/wanted-person-location-intelligence.md` before performing any person-location inference.

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
- **Guarded:** usernames, public-person research, purpose-bound private-person profiling, email/phone exposure checks, breach status, social graphing, threat actors, dark-web references, and verified official wanted/fugitive-person location intelligence.
- **Disallowed:** credentials, doxxing, stalking, covert tracking outside the official wanted-person exception, private-account access, deanonymization for harassment, abusive or invasive dossier building, targeted surveillance of vulnerable people, continuous live person tracking, or illegal access.

For guarded work, narrow scope, prefer first-party or official sources, and redact unnecessary PII. For wanted/fugitive cases, do not infer location until the dedicated activation gate has passed.

### 2. Build a collection plan

Choose the matching workflow:
- `workflows/domain-infrastructure.md`
- `workflows/company-org.md`
- `workflows/username-social.md`
- `workflows/people-public-interest.md`
- `workflows/wanted-person-location-intelligence.md`
- `workflows/email-phone-defensive.md`
- `workflows/image-video-geolocation.md`
- `workflows/news-fact-check.md`
- `workflows/threat-intelligence.md`
- `workflows/monitoring.md`

Route directly to `workflows/wanted-person-location-intelligence.md` only when all activation conditions are satisfied: active official wanted/fugitive status, strong identity match, adult target, lawful public-safety purpose, and public/lawfully supplied evidence. Otherwise remain in `workflows/people-public-interest.md` and do not infer current location.

Start from hypotheses and questions, not tools. Define what evidence would confirm or falsify each hypothesis.

Create two explicit queues before deep searching:

- **Primary-evidence queue:** original files, direct URLs, embedded assets, metadata, source code, archives, attachments, alternate representations, and source-provided hints that have not yet been tested.
- **Hypothesis ledger:** each candidate explanation with its supporting evidence, contradictions, falsifier, confidence, and status (`open`, `leading`, `contradicted`, `verified`).

For image/video tasks, first read `references/visual-clue-taxonomy.md` and create a clue inventory from `templates/visual-clue-inventory.csv`. Do not let the first readable sign, plaque, face, logo, QR payload, or reverse-image hit become the answer.

For structured visual carriers such as QR codes, barcodes, steganographic layouts, or deliberately transformed puzzle artifacts, preserve every reproducible decode separately and test source-signaled transformations such as rotation, mirror, inversion, threshold/channel changes, or alternate layers before treating one valid payload as exhaustive.

### 3. Choose the next action, then its tools

Compare a small set of feasible actions against the current evidence gap. Convert
the leading hypothesis's **fastest falsifier** into an executable source/artifact
check before deepening that branch; execute it or explain why a different action
has greater expected value. Rank qualitatively by discrimination, source fit,
cost, repetition and fidelity after applying scope/access/safety constraints.

Log the expected discriminator, actual result and resulting evidence change.
When rephrased queries return the same source lineages without narrowing the
question, consider an original artifact, representation/habitat pivot, documented
technique transfer, method search, or deterministic/manual fallback. Changing a
query or website alone is not progress. No fixed action count or tool order is
required. Use `templates/strategy-checkpoint.md` only when it helps a branch decision.

For historical questions, current representations are discovery leads until the
required time is verified. Park unexplained clues with revisit triggers. Task
wording, AI output and generatively reconstructed detail are not factual evidence.

The catalog helps implement the selected action; its rankings are not a case plan.

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

Work the primary-evidence queue before expanding a weak lead into broad web search. A search-engine match must not outrank an unresolved original artifact that could directly answer or falsify the question.

Pivot only on corroborated identifiers. Keep a pivot log so aliases, dates, domains, hashes, and locations do not become mixed across entities.

When a public-source collection route hits a CAPTCHA, classify it as an access barrier. Try lawful alternate public routes first. If the site presents ordinary human verification, pause for an operator checkpoint and resume only after the operator completes the challenge manually. Do not automate CAPTCHA solving or transfer verification/session material between environments.

For official wanted/fugitive-person cases, build a location timeline that separates source time, content time, inferred place, and freshness. Do not turn a historical or reposted clue into a current-location claim.

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
- For official wanted/fugitive-person cases, current notice status and whether the location evidence is historical, last-known, recent-lead, or unresolved

For every leading hypothesis, explicitly ask:
- What is the strongest evidence **against** it?
- What unprocessed first-party evidence could overturn it?
- Is the apparent corroboration genuinely independent, or is it one clue echoed through search results?
- What is the cheapest next test that could falsify it?

Use `references/evidence-confidence.md` and `references/hypothesis-convergence.md` for the scoring and state-transition rules.

### 6. Convergence gate and retry loop

Do not produce a submission-safe final answer until all of the following are true:

- [ ] The exact question and required output format are resolved.
- [ ] Material first-party artifacts and explicit source-provided hints have been processed, or documented as inaccessible/irrelevant.
- [ ] Relevant alternate representations or transformations of the original evidence have been tested when signaled by the source or artifact structure.
- [ ] The leading hypothesis is supported by evidence stronger than search coincidence, thematic similarity, or a single clue lineage.
- [ ] At least one deliberate falsification attempt has been performed against the leading hypothesis.
- [ ] Credible contradictions are resolved or clearly bounded.
- [ ] No unresolved primary evidence could plausibly overturn the final answer.
- [ ] The answer is backed by the highest-authority source reasonably available.

For official wanted/fugitive-person location findings, also require the dedicated workflow's official-status recheck, freshness label, confidence, and strongest contradiction/falsification attempt before finalizing.

If the gate fails, continue investigating instead of guessing a precise answer.

If an answer is rejected or a new source contradicts it:

1. Record the rejection/contradiction as evidence.
2. Revert to the last verified checkpoint.
3. Mark the affected hypothesis `contradicted` or lower its confidence.
4. Reopen the primary-evidence queue and unresolved discriminators.
5. Change one assumption or branch at a time.
6. Repeat collection → verification → falsification → gate until the evidence state changes.

This is an investigation loop, not a wording-bruteforce loop.

### 7. Preserve evidence

Initialize a ledger:

```bash
python scripts/evidence_ledger.py init case/evidence.csv
python scripts/evidence_ledger.py add case/evidence.csv \
  --claim "Example claim" \
  --source-url "https://example.org/source" \
  --source-title "Example source" \
  --source-type primary \
  --confidence medium \
  --notes "What this source supports and what it does not"
```

For local files, record hashes. Do not store unnecessary sensitive data.

### 8. Report

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
- **Open hypothesis**
- **Single-source lead**
- **Contradicted**
- **Unresolved / unknown**

For official wanted/fugitive-person cases, use the required output fields in `workflows/wanted-person-location-intelligence.md`, including notice source, status-check time, location finding, evidence timestamps, freshness, confidence, supporting sources, strongest contradiction, and handling note.

Use the user's language. Avoid dramatic wording; precision beats certainty theater.

## Operating modes

### Quick tool selection
Return 3–7 tools, grouped by investigation stage. For each: purpose, why it fits, risk/registration caveat, and fallback.

### Investigation plan
Return hypotheses, collection stages, source priorities, verification tests, stop conditions, and deliverables. Do not pretend collection has already happened.

### Full investigation
Perform the plan, keep an evidence ledger and hypothesis ledger, cite all material claims, and publish a confidence-rated report only after the convergence gate passes.

### Verification / fact-check
Trace the claim to its earliest available source, validate media provenance, compare independent reporting, identify missing context, attempt falsification, and state a verdict with confidence.

### Official wanted/fugitive location intelligence
Activate only for an adult with a current official wanted/fugitive notice and a strong identity match. Use public or lawfully supplied evidence to infer a bounded last-known or recently evidenced location, attach freshness and confidence, recheck official status before finalizing, and stop immediately if the notice is no longer active or only prohibited collection routes remain. Never convert this mode into continuous live surveillance or tactical apprehension guidance.

### Monitoring
Define entities, keywords, negative keywords, feeds, cadence, alert threshold, deduplication, and escalation criteria. Do not monitor private individuals invasively. The official wanted/fugitive workflow does not authorize continuous minute-by-minute monitoring.

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
- Hypothesis and convergence control: `references/hypothesis-convergence.md`
- Adaptive next-action strategy: `references/adaptive-investigation-strategy.md`
- Strategy checkpoint and deferred clues: `templates/strategy-checkpoint.md`
- Optional trace audit / evaluation limits: `references/trajectory-evaluation.md`
- Visual clue taxonomy: `references/visual-clue-taxonomy.md`
- Image/video workflow: `workflows/image-video-geolocation.md`
- Official wanted/fugitive workflow: `workflows/wanted-person-location-intelligence.md`
- Visual clue ledger: `templates/visual-clue-inventory.csv`
- Candidate scoring matrix: `templates/location-candidate-matrix.csv`
- Image geolocation report: `templates/image-geolocation-report.md`
- Other report templates: `templates/`
