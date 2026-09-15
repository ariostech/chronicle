# Chronicle Governance

## Purpose

This document explains how Chronicle is stewarded, how contributors gain responsibility, and how project decisions are made.

Chronicle is an open-source project under the stewardship of Arios Technologies Inc. Stewardship means Arios protects the project's purpose, legal identity, and long-term continuity. It does not mean outside contributions are merely suggestions: technical authority should become broader as sustained contributors earn trust.

## Principles

- Decisions are made in public unless security, privacy, legal, or personnel concerns require confidentiality.
- Technical arguments are judged on evidence, impact, and consistency with Chronicle's charter.
- Authority is earned through sustained, constructive work and can be removed when it is no longer exercised responsibly.
- A maintainer's employer does not make an argument stronger or weaker.
- Security, authorization, provenance, portability, and open-source completeness are project constraints, not optional enhancements.
- Project roles grant responsibility, not ownership of community work.

## Roles

### Contributor

Anyone who participates constructively through code, documentation, design, testing, issue triage, research, review, or community support.

### Reviewer

A contributor trusted to review changes in a defined area. Reviewers may approve work, but merge permission is not implied.

Reviewer expectations:

- understand the relevant specification and tests;
- disclose conflicts of interest;
- distinguish required changes from personal preference;
- respond reliably or step back when unavailable;
- protect confidential security reports.

### Maintainer

A contributor with merge authority in one or more areas. Maintainers are responsible for quality, compatibility, security, and the health of the review process.

Maintainers may:

- merge or close pull requests;
- triage and label issues;
- approve routine releases within their area;
- sponsor new reviewers;
- participate in formal project decisions.

### Security maintainer

A maintainer explicitly trusted to receive private vulnerability reports, coordinate fixes, and approve security releases. This role requires confidentiality and should remain small.

### Lead maintainer

The lead maintainer resolves process deadlocks, represents the project's stewardship responsibilities, and confirms appointments or removals. At project formation, Arios Technologies appoints the lead maintainer.

The lead maintainer cannot waive the license, secretly redefine the project's public contracts, or treat the governance process as optional.

## Areas of responsibility

Maintainer responsibility may be scoped, for example, to:

- protocol and public specifications;
- authorization and security;
- memory providers;
- OKF and knowledge governance;
- MCP and SDKs;
- deployment and operations;
- documentation and community.

`MAINTAINERS.md` records current roles and scopes. `CODEOWNERS` routes reviews but does not replace this governance policy.

## Appointments

A reviewer or maintainer candidate should show sustained work, sound judgment, respectful collaboration, and understanding of Chronicle's purpose and safety boundaries.

Appointments require:

1. a public nomination by a maintainer;
2. at least seven calendar days for maintainer feedback;
3. no unresolved substantiated objection;
4. confirmation by the lead maintainer;
5. an update to `MAINTAINERS.md`.

Early in the project, there may be too few maintainers for independent approvals. This must be stated plainly rather than simulated through empty process.

## Inactivity and removal

Maintainers should announce extended unavailability when practical. A maintainer who has not participated for six months may be moved to emeritus status after private outreach and a 30-day response window.

A role may be suspended or removed for:

- repeated disregard of security or review requirements;
- abuse of access;
- serious or repeated Code of Conduct violations;
- undisclosed conflicts that distort decisions;
- persistent inability to perform the role.

Urgent access suspension may happen immediately when repository or user safety is at risk. Permanent removal follows documented review by disinterested maintainers and confirmation by the lead maintainer. When the lead maintainer is involved, Arios Technologies appoints a disinterested decision-maker.

## Decision classes

### Routine changes

Bug fixes, clarifications, tests, documentation improvements, dependency maintenance, and changes within accepted contracts use ordinary pull-request review.

One qualified approval is normally enough. Security-sensitive or cross-boundary changes should receive approval from the relevant owner.

### Architectural decisions

Choices among concrete implementation options that do not redefine Chronicle's public purpose use an Architecture Decision Record (ADR).

Examples include the primary language, queue library, or initial authorization engine.

### Material changes

Changes to public contracts, trust boundaries, governance, licensing, compatibility promises, persistence semantics, or the Chronicle OKF profile require a Request for Comments (RFC). An accepted RFC normally produces one or more ADRs when implementation choices are made.

### Security decisions

Vulnerability handling may happen privately until disclosure is safe. Any lasting public contract or architecture change must be documented after the embargo ends, with sensitive exploit details omitted when necessary.

## Decision process

Chronicle uses lazy consensus for ordinary work: a well-described proposal may proceed when qualified reviewers agree and no unresolved technical objection remains.

For an RFC:

1. open a draft pull request containing the RFC;
2. identify affected contracts, security boundaries, migration needs, and alternatives;
3. allow at least 14 calendar days for public review unless the change is urgent;
4. address objections with evidence or record why they remain;
5. obtain approvals from two maintainers when two disinterested maintainers exist, including an owner of each affected area;
6. merge the RFC with status `accepted`, or close it with the reason recorded.

Consensus does not require unanimity. A blocking objection must identify a concrete conflict with the charter, specification, security model, interoperability, compatibility, or a demonstrated operational risk.

If consensus cannot be reached, the lead maintainer decides and records the reasoning. Governance and licensing changes additionally require Arios Technologies' approval as project steward.

## Appeals

A contributor may request reconsideration when they believe a decision ignored material evidence or the documented process. The request should identify the specific decision, missing evidence, and requested remedy.

Disinterested maintainers review the appeal. The final outcome and rationale are recorded publicly unless confidentiality is required.

## Conflicts of interest

Maintainers must disclose financial, employment, personal, or competitive interests that a reasonable participant could view as affecting judgment. Disclosure does not always require recusal, but undisclosed conflicts are unacceptable.

A maintainer should not be the sole approver for a change that directly privileges their commercial service, employer, or proprietary product.

## Releases

Release authority and the required checks are defined in `RELEASING.md`. No single maintainer should both introduce and release a security-sensitive change when another qualified maintainer is available.

## Changes to governance

Governance changes require an RFC, a minimum 14-day review, approval from two maintainers when available, and confirmation by Arios Technologies as steward.

The history of this file is part of the governance record.
