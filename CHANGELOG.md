# Changelog

## Unreleased

- Added a guarded `wanted-person-location-intelligence` workflow for adults covered by an active official wanted/fugitive notice
- Added an activation gate requiring official status verification, identity matching, lawful purpose, adult target status, and public/lawfully supplied evidence
- Enabled bounded public-source location inference for verified wanted-person cases, including recent-location clue correlation and exact geolocation when evidence supports it
- Added mandatory freshness labels, confidence, contradiction/falsification checks, and official-status rechecks before finalizing a location finding
- Preserved hard boundaries against private-account access, credential/breach data, device/carrier/brokered telemetry, deception, third-party contact, continuous live surveillance, and tactical apprehension guidance

## 1.2.0

- Added a mandatory primary-evidence queue so unresolved first-party artifacts block final convergence
- Added an explicit hypothesis ledger with support, contradictions, falsifiers, independence, and state transitions
- Added a convergence gate that separates plausible/high-confidence findings from submission-safe final answers
- Added a rejection/retry loop modeled on agentic test-fail-inspect-revise-retest behavior; rejected answers now reopen evidence instead of encouraging wording brute force
- Added structured visual-carrier handling for alternate QR/barcode/layered-artifact decodes when rotation, mirror, inversion, or other transformations are source-signaled or structurally motivated
- Added `references/hypothesis-convergence.md` with a reusable investigation state machine and premature-convergence controls
- Hardened the evidence-confidence rubric against search-coincidence clusters and unprocessed primary evidence

## 1.1.1

- Added lawful human CAPTCHA checkpoints without allowing automated CAPTCHA circumvention or verification-token handling
- Clarified purpose-bound private-person profiling rules and proportionality limits
- Unified package version metadata and release validation around a canonical `VERSION` file

## 1.1.0

- Rebuilt the image/video geolocation workflow around exhaustive clue harvesting before search
- Added a 14-family visual clue taxonomy, uncertain-transcription protocol, and negative-clue collection
- Added parallel search lanes, multi-candidate scoring, source-lineage controls, exact-object matching, and deliberate falsification
- Added a strict camera/object/road geometry gate for exact street and building answers
- Added visual clue, candidate matrix, and image geolocation report templates
- Added a worked example showing how to avoid a single-clue near-match failure

## 1.0.0

- Initial release
- Structured catalog generated from jivoi/awesome-osint
- Added safety gates, nine investigation workflows, search and selection scripts, evidence ledger, templates, and package verification
