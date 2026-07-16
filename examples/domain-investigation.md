# Example — Domain Investigation Plan

## Objective

Assess the public ownership, infrastructure history, and abuse risk of `example.com` without probing or accessing non-public systems.

## Questions

1. What entity controls the domain and when was it registered?
2. Which DNS, certificates, IPs, and ASNs are currently associated?
3. How did the site and infrastructure change over time?
4. Do reputable sources report phishing, malware, or abuse?

## Stages

1. RDAP and registrar records
2. DNS and certificate transparency
3. ASN/BGP and hosting context
4. Web archives and historical content
5. Multi-source reputation and official notices

## Confidence rules

- Registrar/RDAP facts: high when current and directly observed
- Historical ownership: medium unless confirmed by archived records
- Shared infrastructure relationships: lead only
- Abuse verdict: requires multiple reputable sources and timestamps
