# Chronicle Security Policy

## Project status

Chronicle is currently design-stage and pre-alpha. No release is supported for production use. Security reports about the specifications, repository automation, or future implementation are still welcome.

## Supported versions

| Version | Supported |
| --- | --- |
| Unreleased `main` branch | Best effort for repository and design defects |
| Pre-release builds | No security-support guarantee unless a release note says otherwise |
| Stable releases | Not yet available |

This table will change when Chronicle publishes versioned artifacts.

## Reporting a vulnerability

Do not file a public issue or discussion for a vulnerability.

Use [GitHub's private vulnerability-reporting form](https://github.com/ariostech/chronicle/security/advisories/new). If that form is unavailable, contact the repository owner through an official Arios Technologies channel and request a private reporting path without including exploit details in the first public message.

Include, when available:

- the affected version or commit;
- the affected component and configuration;
- a concise description of the impact;
- reproducible steps using synthetic data;
- relevant logs with secrets and personal data removed;
- any suggested mitigation;
- whether you believe the issue is already being exploited or publicly known.

Do not access data that is not yours, degrade a service, persist access, or disclose sensitive information to prove a report.

## Response targets

These are goals, not a service-level agreement:

- acknowledgement within five business days;
- initial triage within ten business days;
- a status update at least every 14 days while an accepted report remains open.

Complex issues may take longer. The security maintainer will coordinate scope, remediation, advisory publication, and credit with the reporter.

## Coordinated disclosure

Please allow maintainers a reasonable period to investigate and publish a fix before public disclosure. Chronicle will not ask reporters to hide unresolved risk indefinitely. The disclosure date should reflect severity, exploit availability, downstream exposure, and the time users need to upgrade.

When appropriate, Chronicle will publish a GitHub Security Advisory, request a CVE, identify affected and fixed versions, describe mitigations, and credit the reporter if they want credit.

## Security release process

Security fixes should:

1. be developed in a private advisory fork when embargo is needed;
2. include a regression test where safe;
3. receive review from a security maintainer and another qualified maintainer when available;
4. update the threat model if the architecture assumption changed;
5. produce patched releases for supported version lines;
6. publish an advisory and release notes with practical upgrade or mitigation instructions.

## Scope priorities

Chronicle gives highest priority to defects involving:

- cross-user, cross-project, cross-organization, or cross-agent disclosure;
- unauthorized durable writes or knowledge approval;
- confused-deputy access;
- memory poisoning or persistent prompt injection that crosses trust boundaries;
- provenance or audit forgery;
- secret retention or unintended model egress;
- deletion or retention failures that expose protected data;
- release, dependency, or build-pipeline compromise.

Retrieval-quality bugs without a security impact belong in the public issue tracker.

## Safe-harbor intent

Chronicle supports good-faith security research that avoids privacy violations, service disruption, social engineering, and access to third-party data. The project intends not to pursue legal action against researchers who follow this policy, act to avoid harm, and provide a reasonable opportunity to fix confirmed issues.

This statement does not authorize testing systems or data operated by third parties.
