# ADR-0001: License Chronicle under Apache License 2.0

- Status: accepted
- Date: 2026-09-11
- Decision owners: Arios Technologies Inc.
- Related issue or RFC: none; records the repository's founding decision
- Supersedes: none
- Superseded by: none

## Context

Chronicle is intended to be usable as a real self-hosted system, including its security, governance, audit, and integration capabilities. Its license must permit commercial use, modification, redistribution, and hosted operation while giving contributors and adopters a clear patent grant.

## Decision drivers

- broad use by individuals, companies, and service providers;
- an explicit patent license and termination terms;
- compatibility with the initial Hindsight provider and the OKF ecosystem;
- familiar compliance obligations for open-source adopters;
- preservation of copyright and attribution notices.

## Options considered

### Apache License 2.0

Permissive use with an express patent grant, contribution terms, and notice requirements. It is widely understood but requires distributors to preserve license and applicable notice material.

### MIT License

Short and permissive, but without Apache-2.0's explicit patent language and NOTICE mechanism.

### Reciprocal licenses

Copyleft and network-copyleft licenses can protect downstream openness, but would narrow some integration and adoption paths. Chronicle's open-core commitment is being expressed through governance and release scope rather than reciprocal licensing.

## Decision

Chronicle source and project documentation are licensed under Apache License 2.0 unless a file or third-party component clearly states otherwise.

## Consequences

### Positive

- users may run, modify, redistribute, and offer Chronicle as a service;
- contributors and users receive the license's express patent grant;
- the license aligns with several relevant upstream projects and standards implementations.

### Negative

- permissive licensing does not require downstream services to publish modifications;
- releases must preserve license, copyright, and applicable notice information.

### Risks and follow-up

- dependency review must prevent incompatible code from entering the repository;
- release automation should include license and notice files;
- vendored or generated content must retain its own attribution and license.

## Security and privacy impact

The license does not enforce Chronicle's security promises. Authentication, authorization, audit, safe defaults, and self-hosting remain open-source product requirements under the charter. No identity, retention, or data-egress behavior changes through this decision.

## Compatibility and portability

Apache-2.0 permits Chronicle to integrate with permissively licensed components. Every dependency remains subject to individual compatibility review. This ADR does not relicense third-party fixtures, models, data, or provider software.

## Validation

The repository contains an unmodified Apache License 2.0 text and an appropriate `NOTICE`. CI checks for both files. Revisit this decision only through a governance-approved RFC with legal review.
