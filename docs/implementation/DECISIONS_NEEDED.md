# Chronicle Decisions Needed

This file tracks choices that require an explicit decision instead of an invisible implementation assumption.

## Foundational decisions for Phase 01

| Decision | Current constraint | Required artifact |
| --- | --- | --- |
| Runtime language and web framework | Must support server, worker, MCP, migrations, observability, and one-image deployment; maintainer experience matters | ADR |
| Admin UI framework | Must remain maintainable, accessible, and distributable with the first-party image | ADR or part of runtime ADR |
| PostgreSQL ownership boundary | Chronicle and Hindsight need separate ownership and migration responsibility | ADR |
| Authorization model and engine | Must model human + agent/workload + delegation + action + resource + scope | ADR and `AUTHORIZATION.md` |
| Async job mechanism | Default Compose should stay small; durable semantics are required | ADR |
| Hindsight bank mapping | Isolation must be proven, not represented only by tags | ADR and `PROVIDER_INTERFACE.md` |
| Chronicle OKF profile | Extend upstream OKF without forking it | ADR and `OKF_PROFILE.md` |
| Knowledge bundle boundaries | Git clone/history semantics must match access boundaries | ADR |
| MCP transport and authorization | Must preserve workload identity and current MCP authorization semantics | ADR and `MCP.md` |
| Initial local-model profile | Must work on realistic developer hardware without weakening egress policy | ADR |

## Decision method

For each choice, record requirements, realistic alternatives, operational cost, security/privacy impact, portability, migration path, and evidence that would cause reconsideration. Prefer the smallest boring choice that satisfies Chronicle's written contracts.

Do not use this file as the decision record. Once accepted, link the ADR here and move the item to a completed section.

## Completed decisions

- Apache License 2.0 — [ADR-0001](../adr/0001-apache-2.0-license.md)
- Standard-library Python for benchmark v0.1 only — [ADR-0002](../adr/0002-python-benchmark-harness.md)
