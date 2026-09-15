# Architecture Decision Records

Architecture Decision Records (ADRs) capture concrete technical choices and their consequences.

Use an ADR when Chronicle needs to choose among implementation options without redefining the project's purpose or public governance. Use an RFC first when a choice changes a public contract, trust boundary, persistence semantics, compatibility promise, or governance.

## Process

1. Copy `TEMPLATE.md` to the next available number, such as `0001-primary-language.md`.
2. Set the status to `proposed` and open a pull request.
3. Link the issue or RFC that created the decision.
4. Record the real alternatives and security consequences.
5. After approval, change the status to `accepted` and merge it.

Accepted ADRs are not edited to make history look cleaner. A later choice supersedes an earlier ADR through a new ADR that links both directions.

## Status values

- `proposed`
- `accepted`
- `rejected`
- `deprecated`
- `superseded by ADR-NNNN`

## Initial sequence

The Reference Architecture proposes these first decisions:

1. license choice — accepted in [ADR-0001](0001-apache-2.0-license.md);
2. benchmark harness language — accepted in [ADR-0002](0002-python-benchmark-harness.md);
3. primary implementation language and framework;
4. Hindsight provider boundary;
5. PostgreSQL ownership and database separation;
6. authorization model and engine;
7. Chronicle profile for OKF v0.2;
8. knowledge-bundle boundary strategy;
9. async job mechanism;
10. MCP transport and authentication;
11. local-model profile.

The benchmark harness ADR deliberately does not settle the production runtime language.
