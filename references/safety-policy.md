# Safety and Privacy Policy

## Purpose

This skill supports lawful, ethical research from public and authorized sources. OSINT does not mean “anything found online is fair game.” Availability, necessity, proportionality, and likely harm all matter.

## Allowed

- Verifying public claims, documents, images, videos, and timelines
- Researching organizations, domains, infrastructure, public filings, official records, and published threat reports
- Defensive exposure checks for accounts, domains, or systems owned by the user or covered by explicit authorization
- Research about public figures when relevant to public duties or a clear public-interest question
- Mapping public corporate, technical, or institutional relationships

## Guarded

Apply data minimization, narrow scope, and stronger verification to:

- Username and account discovery
- Purpose-bound profiling of private individuals using public or authorized sources
- Email and phone research
- Public-record and people-search services
- Social-network analysis
- Breach, leak, dark-web, or threat-actor references
- Location inference from media
- Facial or biometric tools
- Official wanted/fugitive-person location intelligence

For guarded work:

1. Confirm legitimate purpose or authorization.
2. Keep private-person profiling tied to a specific investigation objective and collect only what is necessary to answer it.
3. Avoid collecting home address, family members, personal phone numbers, real-time location, sensitive traits, or unrelated accounts unless there is a compelling lawful and proportionate need covered by a narrower approved workflow.
4. Do not turn a bounded investigation into a comprehensive life dossier.
5. Redact unnecessary identifiers from notes and reports.
6. Prefer exposure status, official records, and remediation over raw sensitive data.
7. Stop when the objective is met.

## Official wanted/fugitive-person exception

A narrow public-safety exception exists for **adults who are currently named in an active, official wanted/fugitive notice** issued by a recognized government, court, prosecutor, police, or international law-enforcement authority.

This exception is intended for lawful apprehension support, verification of public location clues, and preparation of an official tip. It does not convert the skill into a general-purpose people tracker.

Before enabling the exception:

1. Verify the current official wanted/fugitive notice from the issuing authority.
2. Confirm the target identity strongly enough to avoid namesake or lookalike errors.
3. Confirm the target is an adult and the notice remains active.
4. Limit collection to public, lawfully accessible, or operator-supplied evidence.
5. Use `workflows/wanted-person-location-intelligence.md` and preserve source, timestamp, freshness, confidence, and contradictions.

Once those conditions pass, the skill may infer a **last-known or recently evidenced location** from public evidence, including geolocation of public photos/videos and correlation of timestamps, landmarks, transport clues, events, weather, signage, road geometry, and other scene evidence. An exact place or coordinates may be reported only when the evidence supports it and the result is clearly labeled with freshness and confidence.

The exception does **not** allow:

- Private-account access or authentication bypass
- Device, carrier, cell-site, hidden telemetry, or brokered GPS/ad-location tracking
- Credential, breach-dump, stealer-log, or leaked-private-message use
- Contacting, deceiving, impersonating, phishing, calling, messaging, or socially engineering the target or third parties
- Tracking relatives or associates merely as a route to the target unless they independently pass the same official-wanted-person gate
- Continuous minute-by-minute live surveillance
- Tactical interception, confrontation, raid, weapon, or apprehension instructions

If the official notice is withdrawn, the person is reported arrested/surrendered/deceased, identity becomes uncertain, or only prohibited collection routes remain, stop the location investigation immediately.

## Access barriers and human checkpoints

A CAPTCHA or equivalent human-verification challenge is an access barrier, not an automatic mission stop.

- First try lawful alternative public routes such as official APIs, server-rendered public pages, search indexes, archives, or independent public sources.
- When the site offers ordinary human verification, the agent may pause and ask the operator to complete the CAPTCHA manually through the normal browser interface.
- After the operator confirms successful verification, the investigation may resume in that same authorized browser session if the underlying task remains permitted.
- The agent must not automate CAPTCHA solving or circumvention, use third-party solving farms, or extract, export, replay, transfer, or reuse CAPTCHA tokens, session cookies, authentication material, or other verification artifacts.
- A login wall, paywall, rate limit, robots control, or other access control must not be bypassed merely because a human checkpoint is available.

## Disallowed

- Obtaining, guessing, validating, or exposing passwords, tokens, session cookies, or private keys
- Buying, downloading, sharing, or searching raw credential dumps for personal data
- Doxxing, stalking, harassment, intimidation, blackmail, or revenge
- Real-time tracking of a person, vehicle, vessel, or device for harmful purposes; official wanted-person work is limited to the bounded public-source workflow above and is not a general live-tracking exception
- Automated CAPTCHA bypass or circumvention, bypassing authentication, paywalls, rate limits, robots controls, or other access controls
- Accessing private accounts or impersonating someone
- Abusive or invasive profiling that is unrelated or disproportionate to a legitimate investigation objective
- Identifying a private person by face or enabling biometric surveillance
- Targeting minors or vulnerable people
- Inferring sensitive traits such as health, sexuality, religion, ethnicity, or political affiliation without a compelling lawful/public-interest basis
- Malware execution, phishing, exploitation, or operational intrusion

## Breach and dark-web rule

Only defensive use is permitted. Acceptable output:

- Whether an owned identifier appears exposed
- Approximate breach date and service name from reputable notice sources
- Risk assessment and remediation steps

Never output:

- Passwords or password hashes
- Full breach records
- Stealer-log contents
- Private communications
- Instructions to obtain or trade leaked data

## Source and tool risks

The catalog contains third-party links. Some may be dead, deceptive, unsafe, invasive, or unlawful in a jurisdiction. Before use:

- Verify the domain and current reputation
- Prefer official project pages and source repositories
- Use an isolated browser profile for unknown sites
- Do not upload sensitive evidence to third-party services without permission
- Review terms, retention, and jurisdiction
- Avoid installing unknown binaries
- Treat “free” and “no signup” labels as unverified hints

## Escalation

When a request mixes legitimate and harmful goals, provide the safe subset: public facts, defensive exposure status, privacy-preserving verification, bounded official wanted-person location intelligence, or remediation. Explain the boundary clearly.
