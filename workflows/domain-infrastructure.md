# Domain and Infrastructure Workflow

## Questions

- Who currently controls the domain, and what historical ownership signals exist?
- What DNS, certificate, ASN, hosting, and related-domain relationships are visible?
- How has the site changed over time?
- Are there reputable abuse, phishing, or malware indicators?

## Stages

1. **Identity:** RDAP/WHOIS, registrar, nameservers, registration dates.
2. **DNS and certificates:** A/AAAA/MX/NS/TXT, certificate transparency, subdomains.
3. **Infrastructure:** IP, ASN, BGP, hosting/CDN, passive DNS when authorized.
4. **Content history:** current site, robots/sitemaps, archives, historical screenshots.
5. **Technology and relationships:** frameworks, analytics IDs, linked domains; treat shared hosting carefully.
6. **Reputation:** official CERT/vendor reports and multiple independent reputation sources.

## Verification traps

- Privacy-proxy registrant data is not the owner.
- Shared IP or analytics IDs do not prove common control.
- Current DNS does not establish historical state.
- Scanner labels are leads, not verdicts.
