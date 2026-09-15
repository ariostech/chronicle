# Chronicle

Chronicle is an open-source platform for governed organizational memory.

It gives people and AI agents durable context without treating every model output as truth. Chronicle separates machine memory from reviewed institutional knowledge, preserves provenance and time, enforces scope before retrieval or write, and keeps approved knowledge portable as Markdown using the Open Knowledge Format (OKF) and Git.

> **Project status:** design and pre-alpha. The contracts are being specified before the runtime is implemented. Do not use Chronicle for production data yet.

## Why Chronicle exists

Most agent-memory systems answer one part of the problem: how an agent stores and recalls past information. Organizations need a longer chain:

```text
source or event
  -> machine memory
  -> evidence-backed observation
  -> candidate knowledge
  -> human review
  -> institutional knowledge
  -> future action
```

Chronicle governs that chain. It carries identity, authorization, scope, provenance, authority, temporal validity, retention, and audit information through the lifecycle.

## The product model

Chronicle distinguishes four layers:

| Layer | Role | Canonical home |
| --- | --- | --- |
| Working context | Immediate task and conversation state | Agent/model context |
| Machine memory | Experiences, facts, observations, and learned context | Replaceable memory provider; Hindsight initially |
| Institutional knowledge | Reviewed, durable, human-readable organizational knowledge | OKF-compatible Markdown in Git |
| Systems of record | Authoritative operational state | Existing databases, applications, documents, and APIs |

Machine memory may inform work. It does not silently become organizational truth.

## Design commitments

- Authorize before disclosure and before durable writes.
- Treat human and agent identities as distinct principals.
- Preserve provenance through extraction, consolidation, and promotion.
- Model time as part of the fact, including supersession and historical state.
- Keep canonical institutional knowledge readable without Chronicle.
- Put memory engines and model providers behind explicit interfaces.
- Keep governance, audit, authorization, self-hosting, and local-model support in the open-source core.
- Make a useful local deployment possible with a maintained Docker Compose stack.

## Current architecture direction

The first implementation is expected to combine:

- a Chronicle gateway and API as the trust boundary;
- a worker for capture, consolidation, indexing, retention, and knowledge proposals;
- an MCP server for agent access;
- Hindsight behind Chronicle's memory-provider contract;
- OKF-compatible knowledge bundles backed by Git and usable from Obsidian;
- PostgreSQL with isolated Chronicle and provider ownership boundaries;
- optional local-model, collaboration, and observability profiles.

The implementation language, authorization engine, queue, and several provider mappings remain open. They will be chosen through ADRs and validated against the threat model and proof-of-concept requirements.

## Project documents

- [Project Charter](docs/project/PROJECT_CHARTER.md)
- [Technical Specification v0.1](docs/spec/TECHNICAL_SPECIFICATION.md)
- [Reference Architecture](docs/architecture/REFERENCE_ARCHITECTURE.md)
- [Security and Threat Model](docs/security/THREAT_MODEL.md)
- [Benchmark Specification v0.1](docs/spec/BENCHMARK.md)
- [Benchmark Harness](packages/benchmark/README.md)
- [Claude Code implementation prompt suite](docs/implementation/claude-code/README.md)
- [Implementation Status](docs/implementation/STATUS.md)
- [Roadmap](ROADMAP.md)
- [Governance](GOVERNANCE.md)
- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Release Policy](RELEASING.md)
- [Writing Guide](WRITING.md)

Architectural decisions live in [`docs/adr/`](docs/adr/README.md). Proposals that need wider design review live in [`docs/rfc/`](docs/rfc/README.md).

## What is usable today?

The repository contains the project's governing documents, contribution foundation, and an executable provider-neutral benchmark harness. Runtime services and deployment artifacts have not been implemented yet.

Run the deterministic contract and security suite with Python 3.11 or later:

```bash
PYTHONPATH=packages/benchmark/src \
  python3 -m chronicle_bench run \
  --suite packages/benchmark/fixtures/v0.1/contract.json
```

The suite covers retrieval, temporal updates, historical queries, entity aliases, abstention, scope isolation, delegated authority, unauthorized writes, synthetic secret screening, untrusted retrieved instructions, poisoning, staleness, approval separation, provenance, deletion, provider outages, and context budgets. Security failures are disqualifying rather than averaged into a quality score.

The repository also contains a staged, Opus 5-optimized [Claude Code implementation suite](docs/implementation/claude-code/README.md). It covers the remaining architecture decisions and contracts, runtime, authorization, Hindsight, OKF/Git, retrieval, MCP, promotion, administration, Docker/local AI, security, operations, evaluation, documentation, and final alpha acceptance. The prompts do not imply those runtime capabilities are already implemented.

The first runtime milestone is a narrow end-to-end proof:

1. validate and index approved OKF knowledge from Git;
2. retrieve it through an authorized MCP request;
3. retain project-scoped experience through Hindsight;
4. turn supported observations into a candidate OKF change;
5. review and merge the change in Git;
6. retrieve the approved knowledge in a fresh agent session with traceable evidence.

## Contributing

Chronicle is early, so design contributions are as valuable as code. Start with [CONTRIBUTING.md](CONTRIBUTING.md), search existing issues and RFCs, and open a proposal before investing in a large change.

All commits must include a Developer Certificate of Origin sign-off. Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Do not report vulnerabilities in a public issue. Follow [SECURITY.md](SECURITY.md) and use the repository's private vulnerability-reporting channel.

## License

Chronicle is licensed under the [Apache License 2.0](LICENSE).

Copyright 2026 Arios Technologies Inc. and Chronicle contributors.
