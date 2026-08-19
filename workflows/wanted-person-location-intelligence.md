# Wanted-Person Location Intelligence — Official Public-Safety Cases Only

This workflow is a guarded exception for locating **adults who are currently named in an active, official wanted/fugitive notice** issued by a recognized public authority (for example, a national police service, court, prosecutor, INTERPOL, Europol, or equivalent government agency).

It is designed for lawful public-safety investigations, official tip preparation, and verification of public-source location leads. It does **not** authorize covert access, device tracking, account intrusion, deception, or continuous surveillance.

## Activation gate

Do not enable this workflow unless all of the following are true:

1. **Official status:** the target is named in a current official wanted/fugitive notice or warrant-related public bulletin.
2. **Identity match:** name, photo/description, case identifiers, and issuing authority are consistent enough to avoid a namesake mix-up.
3. **Adult target:** the target is not a minor or otherwise specially vulnerable person.
4. **Lawful purpose:** the objective is apprehension support, public-safety research, an official tip, or verification of a location clue tied to the active notice.
5. **Source boundary:** collection is limited to public, lawfully accessible, or operator-supplied evidence. No authentication bypass, private-account access, stolen data, brokered location telemetry, or credential material.

If any gate item fails, fall back to `people-public-interest.md` and do not perform person-location inference.

## What becomes available

Once the activation gate passes, the investigator may perform **bounded public-source location intelligence** that would normally be too invasive for ordinary private-person research:

- Geolocate public photos or videos associated with the wanted person.
- Correlate recent public timestamps, landmarks, signage, road geometry, weather, events, transport clues, and other scene evidence.
- Compare public posts, official releases, reputable reporting, and archives to estimate a **last-known or recently evidenced location**.
- Resolve whether multiple public sightings are the same place, different places, reposts, or stale material.
- Produce an exact place or coordinates **only when supported by the evidence**, with timestamp/freshness and confidence attached.
- Build a concise tip packet containing the target identity basis, location finding, source URLs, timestamps, screenshots/notes, contradictions, and confidence.
- Check for an official arrest/custody/status update before finalizing so the investigation stops when the notice is no longer active.

This is location **inference from evidence**, not a license for live surveillance.

## Still prohibited

Even in this mode, do not:

- Access private accounts, messages, cloud data, devices, carrier records, or non-public databases without an explicitly integrated authorized system.
- Use passwords, session cookies, credential dumps, stealer logs, leaked private communications, or authentication material.
- Purchase or obtain brokered GPS/mobile-ad telemetry, cell-site data, hidden device telemetry, or equivalent non-public location feeds.
- Trick, contact, impersonate, phish, call, message, or socially engineer the target, relatives, associates, employers, hotels, venues, or third parties.
- Track relatives or associates merely to reach the target unless they are independently named in an official wanted notice and pass their own activation gate.
- Build a broad personal-life dossier unrelated to locating the wanted person.
- Provide tactical interception, confrontation, raid, weapon, or apprehension instructions.
- Run continuous minute-by-minute tracking or claim a person is physically present now when the evidence supports only a recent or historical location.

## Investigation sequence

1. **Verify wanted status.** Capture the issuing authority, notice URL, case/warrant identifier if public, publication/update date, and current status.
2. **Lock identity.** Separate the target from namesakes and copied/reposted media.
3. **Collect first-party evidence.** Process supplied media, official bulletins, public posts, embedded metadata, and source hints before broad searching.
4. **Build a location timeline.** Record each location clue with its source time, content time, inferred place, and freshness.
5. **Geolocate and falsify.** Use the image/video workflow, keep competing candidates alive, and reject near matches deliberately.
6. **Assess freshness.** Label findings as historical, last-known, recent lead, or unresolved. Do not silently turn an old clue into a current-location claim.
7. **Recheck official status.** Stop if the target is reported arrested, surrendered, deceased, the notice is withdrawn, or identity becomes uncertain.
8. **Prepare restricted output.** Report the smallest actionable location finding necessary, with confidence, evidence, contradictions, and handling notes.

## Required output fields

- Target and official wanted-status source
- Issuing authority / case identifier when public
- Status checked at
- Location finding
- Evidence timestamp(s)
- Location freshness: `historical` / `last-known` / `recent-lead` / `unresolved`
- Confidence: `low` / `medium` / `high`
- Supporting sources
- Strongest contradiction or falsification attempt
- Privacy / handling note

## Stop conditions

Stop immediately when:

- Official wanted status is no longer active.
- The identity match becomes uncertain.
- The only remaining route requires private access, credential use, purchased telemetry, deception, or interaction with people.
- The requested output shifts from evidence-based location intelligence to operational interception or continuous live tracking.
