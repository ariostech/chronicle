# Chronicle Roadmap

This roadmap describes outcomes, not fixed dates. Chronicle is still validating its contracts, so ordering may change through accepted RFCs and ADRs.

## Completed: project foundation

- establish the Chronicle name, purpose, scope, and open-source commitments;
- define the technical vocabulary and core invariants;
- define the reference architecture and trust boundaries;
- publish the initial threat model;
- establish repository governance and contribution processes.

## Completed: executable benchmark foundation

The benchmark v0.1 foundation turns the memory research and threat model into repeatable tests before Chronicle commits to provider or storage assumptions. It includes:

- a normative benchmark specification and versioned JSON schemas;
- synthetic contract and provider-retrieval fixtures;
- precision, recall, MRR, nDCG, provenance, latency, context-cost, and policy metrics;
- disqualifying gates for scope leakage, unauthorized writes, deletion failures, and approval bypass;
- adversarial cases for poisoning, retained prompt injection, stale sources, delegation, and provider outages;
- a provider-neutral Python harness, deterministic contract adapter, and opt-in Hindsight adapter;
- reproducibility metadata and deterministic outcome digests;
- CI checks across supported Python versions.

The deterministic adapter proves Chronicle semantics and runner behavior; it is not a production quality baseline. Live Hindsight results remain to be published from a disposable test deployment. Scale, storage-growth, long-accumulation, and model-judged context-usefulness suites remain later benchmark increments.

## Next: supporting contract specifications

The broad technical specification also needs implementable subsystem contracts:

- `docs/spec/AUTHORIZATION.md`;
- `docs/spec/PROVIDER_INTERFACE.md`;
- `docs/spec/OKF_PROFILE.md`;
- `docs/spec/MCP.md`;
- `docs/spec/API.md`;
- `docs/spec/BENCHMARK.md` — complete at v0.1.

Authorization, provider, and OKF profile documents must now become implementable contracts before the proof of concept can claim meaningful conformance. The runtime language and framework decision should be recorded alongside that work.

The complete supervised implementation sequence is maintained in the [Claude Code prompt suite](docs/implementation/claude-code/README.md). That suite is an execution aid, not a replacement for ADR, RFC, security-review, or release-approval gates.

## Milestone: repository and runtime skeleton

- choose the primary implementation language and framework through an ADR;
- create server, worker, MCP, OKF, provider, and benchmark package boundaries;
- establish migrations, configuration validation, structured logging, and health endpoints;
- create the maintained Docker Compose development path;
- add language-specific build, test, lint, and CodeQL workflows.

## Milestone: governed memory proof of concept

- implement principal, actor, organization, project, team, and personal scopes;
- implement explicit read/write authorization at the Chronicle boundary;
- implement the Hindsight provider adapter for health, retain, recall, and provider mappings;
- discover, validate, index, and search an OKF knowledge bundle;
- assemble authorized knowledge and memory within a declared context budget;
- expose the smallest useful MCP tool set;
- create candidate OKF changes from evidence-backed observations;
- support Git review and approval without treating candidates as stable knowledge.

## Milestone: security and evaluation

- automate the P0 isolation tests from the threat model;
- test secret screening, source trust, prompt-injection persistence, and approval bypass;
- measure retrieval precision, recall, latency, temporal correctness, provenance completeness, and token overhead;
- run Hindsight against realistic Chronicle scope and retention workloads;
- validate deletion propagation and provider-failure behavior;
- publish a repeatable benchmark harness and baseline results.

## Milestone: usable alpha

- provide one documented Docker Compose quickstart;
- add setup and diagnostic commands;
- add Obsidian-compatible knowledge-bundle guidance;
- document backup, restore, upgrades, and supported configurations;
- publish versioned APIs, MCP semantics, provider contracts, and the Chronicle OKF profile;
- publish signed release artifacts, SBOMs, and provenance attestations where supported.

## Deferred until evidence justifies them

- multi-region or cross-organization federation;
- automatic high-authority knowledge approval;
- a custom graph database;
- a large proprietary connector catalog;
- provider ensembles;
- a custom document editor;
- mobile clients.

See the [Project Charter](docs/project/PROJECT_CHARTER.md) for the MVP boundary and the [Reference Architecture](docs/architecture/REFERENCE_ARCHITECTURE.md) for the proposed build order.
