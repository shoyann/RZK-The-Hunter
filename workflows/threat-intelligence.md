# Defensive Threat-Intelligence Workflow

## Stages

1. Define the indicator: domain, IP, URL, hash, CVE, campaign, malware family, or actor alias.
2. Normalize indicator format and first-seen/last-seen times.
3. Query official CERTs, vendor advisories, and reputable IOC enrichment sources.
4. Correlate passive DNS, certificates, infrastructure, and campaign reports.
5. Map actor names carefully; aliases and vendor naming differ.
6. Separate observed indicators from attribution claims.
7. Record confidence, source independence, and expiry/decay.
8. Produce defensive actions: block/monitor, patch, hunt queries, user communication, and escalation.

## Boundaries

Do not execute malware, exploit systems, obtain credentials, or engage criminal infrastructure. Avoid downloading samples; use hashes and trusted analysis summaries unless a dedicated authorized sandbox is explicitly available.
