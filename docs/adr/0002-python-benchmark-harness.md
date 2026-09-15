# ADR-0002: Use a standard-library Python harness for benchmark v0.1

- Status: accepted
- Date: 2026-09-11
- Decision owners: Arios Technologies Inc.
- Related issue or RFC: [Chronicle Benchmark Specification v0.1](../spec/BENCHMARK.md)
- Supersedes: none
- Superseded by: none

## Context

Chronicle needs executable evaluation before choosing its production runtime stack. The harness must run in local development and CI, produce deterministic machine-readable results, and support provider adapters without forcing the server language decision.

## Decision drivers

- available in common development and CI environments;
- strong support for JSON, HTTP, statistics, hashing, and testing without extra packages;
- easy adapter development for AI and memory systems;
- small bootstrap and supply-chain footprint;
- independence from Chronicle's future server implementation language.

## Options considered

### Standard-library Python

Python provides the required runner, HTTP client, schemas-as-artifacts, and unit-test tooling with no runtime package downloads. It is concise for benchmark and data work. Static typing is limited at runtime, so the harness must validate inputs explicitly.

### TypeScript

TypeScript would offer strong tooling and could align with a future server, but that server choice has not been made. Even a small harness would require a package-manager and dependency bootstrap.

### Shell scripts

Shell would minimize setup for simple smoke tests but is a poor fit for schemas, metrics, adapters, portable JSON output, and unit tests.

## Decision

Benchmark v0.1 will use Python 3.11 or later and only the Python standard library at runtime. The package lives under `packages/benchmark/` and exposes a module CLI.

This decision selects the benchmark implementation only. It does not select the language or framework for the Chronicle gateway, worker, MCP service, or production provider SDK.

## Consequences

### Positive

- the contract suite runs without downloading dependencies;
- fixtures and results remain ordinary JSON;
- adapters can be tested with built-in HTTP and mocking tools;
- CI has a narrow, auditable dependency surface.

### Negative

- JSON Schema validation in v0.1 is performed by explicit application checks in CI unless an optional validator is installed;
- contributors need Python even if Chronicle's runtime later uses another language;
- advanced data analysis may eventually need an optional development dependency group.

### Risks and follow-up

- keep the adapter boundary language-neutral and documented;
- do not let harness-internal models become Chronicle's public runtime API;
- add optional analysis dependencies only through a later ADR;
- revisit Python version support when the project defines its release platform matrix.

## Security and privacy impact

The default runner makes no network request. Live adapters require explicit selection and environment-based credentials. Results redact secrets and store a configuration fingerprint rather than credentials. Fixtures are synthetic. Hindsight runs require an isolated non-production bank.

## Compatibility and portability

The stable artifacts are the versioned JSON suite and result formats, not Python classes. Other languages may implement compatible runners later. Provider adapters must declare capabilities and must not reinterpret skipped security cases as passes.

## Validation

CI must run unit tests and the deterministic contract fixture on supported Python. Revisit the decision if the standard library cannot express the result contract safely, the harness becomes a deployment dependency, or a second implementation exposes ambiguity in the JSON contracts.
