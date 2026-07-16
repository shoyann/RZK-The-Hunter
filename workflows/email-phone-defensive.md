# Email and Phone — Defensive Workflow

Proceed only for identifiers owned by the user, covered by consent, or within explicit organizational authorization.

## Allowed objectives

- Determine whether an identifier appears in reputable breach-notification services.
- Validate domain configuration and deliverability signals.
- Identify spoofing, impersonation, or abuse risk.
- Recommend remediation.

## Stages

1. Confirm ownership/authorization and redact the identifier in notes where possible.
2. Check reputable exposure-notification sources.
3. Review domain email security: SPF, DKIM, DMARC, MX, and abuse contacts.
4. Assess reputation and known impersonation reports.
5. Report service/date/category at a high level, not raw records.
6. Recommend password reset, unique passwords, MFA/passkeys, token revocation, monitoring, and support escalation.

Never reveal passwords, hashes, account-recovery details, stealer logs, or raw breach data.
