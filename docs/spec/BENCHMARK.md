# Chronicle Benchmark Specification v0.1

- Status: draft
- Version: 0.1.0
- Date: 2026-09-11
- Applies to: Chronicle benchmark datasets, adapters, runs, and result artifacts

## 1. Purpose

This specification turns Chronicle's quality and security claims into repeatable tests. It defines what a conforming benchmark case contains, how a run is recorded, which metrics are comparable, and which failures disqualify a result.

The benchmark is not a single leaderboard number. Chronicle sits on a trust boundary. A system that recalls useful facts but leaks another project's data has failed.

## 2. Scope

Version 0.1 covers:

- deterministic contract tests for scope, time, provenance, lifecycle, retention, and promotion;
- provider-level capture and retrieval evaluation;
- a provider-neutral adapter interface;
- a live Hindsight adapter for the capabilities its public API exposes;
- machine-readable fixtures and results;
- retrieval, latency, cost, and security gates;
- reproducibility metadata.

It does not yet define:

- a production Chronicle API adapter;
- model-judged answer quality;
- a universal weighted score;
- production load, disaster-recovery, or penetration testing;
- copied versions of third-party benchmark datasets.

## 3. Design principles

### 3.1 Security is a gate

Cases marked `security_gate: true` MUST pass. Their failures MUST NOT be averaged away by retrieval scores. A published result with any disqualifying failure MUST be labeled non-conforming.

### 3.2 Capabilities are explicit

Adapters MUST declare the operations they support. The runner MUST skip unsupported non-required cases rather than invent a result. A skipped required capability prevents conformance for the relevant profile.

### 3.3 Evaluation layers stay separate

Chronicle uses three profiles:

| Profile | Subject | Required capabilities |
| --- | --- | --- |
| `contract` | Lifecycle semantics and runner correctness | retain, recall, supersede, delete, authorize, promote, simulate outage |
| `provider-retrieval` | A memory provider behind an isolated test namespace | retain, recall |
| `chronicle-gateway` | A deployed Chronicle boundary | all operations required by the selected suite |

The deterministic adapter is the executable reference for `contract`; it is not a claim about production retrieval quality. The Hindsight adapter targets `provider-retrieval`. A future Chronicle HTTP adapter will target `chronicle-gateway`.

### 3.4 Fixtures are synthetic and versioned

Committed fixtures MUST use invented organizations, people, projects, identifiers, and secrets. Real customer data MUST NOT enter the public suite. Fixture changes that alter expected behavior require a new dataset version.

### 3.5 Runs carry their context

Every result MUST record enough information to explain what ran: suite and fixture hashes, adapter and provider versions, configuration fingerprint, seed, execution profile, source revision, runtime, operating system, architecture, latency, skips, and failures.

Secrets and raw credentials MUST NOT appear in result artifacts. Configuration fingerprints MUST be calculated from a redacted allowlist.

## 4. Prior work

Chronicle's case taxonomy draws on established long-memory evaluation ideas without copying their data:

- [LongMemEval](https://github.com/xiaowu0162/LongMemEval) separates information extraction, multi-session reasoning, temporal reasoning, knowledge updates, preferences, and abstention.
- [LoCoMo](https://aclanthology.org/2024.acl-long.747/) evaluates long-running conversational memory across question answering and event understanding.
- [MemoryAgentBench](https://openreview.net/forum?id=YuT3WQ4H23) identifies retrieval, test-time learning, long-range understanding, and selective forgetting as distinct competencies.
- [MemBench](https://github.com/import-myself/MemBench) distinguishes factual and reflective memory as well as participant and observer settings.

Chronicle adds organizational controls that general conversational-memory benchmarks do not make central: principal and resource scopes, delegated authority, provenance, knowledge approval, retention, and deletion propagation.

## 5. Normative language

The words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

## 6. Suite format

A suite is one UTF-8 JSON document validated by `packages/benchmark/schemas/suite.schema.json`.

Top-level fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Result-contract version, currently `0.1` |
| `suite_id` | Stable human-readable identifier |
| `dataset_version` | Version of the fixture contents |
| `description` | Short statement of the suite's purpose |
| `profile` | `contract`, `provider-retrieval`, or `chronicle-gateway` |
| `default_k` | Default retrieval cutoff |
| `cases` | Ordered benchmark cases |

Each case contains:

| Field | Meaning |
| --- | --- |
| `id` | Stable identifier unique within the suite |
| `category` | Quality or security behavior under test |
| `description` | Human-readable intent |
| `security_gate` | Whether failure disqualifies the run |
| `required_capabilities` | Adapter operations needed by the case |
| `operations` | Ordered setup and assertion operations |

## 7. Operation model

### 7.1 Retain

`retain` supplies a memory record with a stable ID, text, scope, valid time, state, authority, provenance, and optional tags. An adapter MUST reject duplicate IDs unless the provider contract explicitly defines idempotent replay.

### 7.2 Recall

`recall` supplies a query, requesting principal, allowed scopes, evaluation time, state filter, and `k`. Expected results include:

- `relevant_ids`: records that should be returned;
- `forbidden_ids`: records that must not be returned;
- `minimum`: case-specific metric thresholds;
- `max_context_tokens`: an optional budget;
- `require_provenance`: whether every returned item needs at least one provenance reference.

A relevant item below the cutoff affects quality metrics. A forbidden item affects the policy-violation count and fails a security gate.

### 7.3 Supersede

`supersede` links an old record to a replacement. Current-time recall MUST exclude the superseded record by default. Historical recall MAY include it when it was valid at the requested time.

### 7.4 Delete

`delete` makes a record unavailable to ordinary recall. A later recall returning that record is a policy violation. Physical erasure and derived-index cleanup are Chronicle gateway responsibilities; provider-only profiles may skip this operation.

### 7.5 Authorize

`authorize` attempts a read or write with a declared principal and resource scope. The expected result is `allow` or `deny`. Denials MUST be observable without disclosing protected content.

### 7.6 Promote

`promote` attempts to move candidate knowledge into a stable authority state. The operation names both actor and verifier. Self-approval or missing review MUST be denied when the case requires separation of duties.

### 7.7 Fail next

`fail_next` injects a provider outage for the following operation. The adapter MUST return an explicit error. The runner MUST fail any adapter that fabricates a successful empty or invented response.

## 8. Case taxonomy

Version 0.1 fixtures SHOULD cover at least:

| Class | Expected behavior |
| --- | --- |
| Fact recall | Return the correct retained fact |
| Preference recall | Preserve a user preference within its permitted scope |
| Knowledge update | Prefer the active replacement for a current query |
| Historical query | Return the fact valid at the requested time |
| Entity aliasing | Find a record through an established alias |
| Abstention | Return no result when the answer is unsupported |
| Project isolation | Never return another project's record |
| User isolation | Never return another user's personal memory |
| Delegation | Respect the narrower effective scope of an agent grant |
| Unauthorized write | Reject a write outside the principal's authority |
| Secret screening | Reject a synthetic credential-like value before retention |
| Prompt-injection persistence | Store retrieved instructions as untrusted data, not authority |
| Poisoning | Do not convert repetition into authority |
| Staleness | Exclude or label material beyond its freshness policy |
| Promotion | Keep candidate knowledge separate until valid review |
| Provenance | Return traceable source references |
| Deletion | Stop returning a deleted record |
| Provider outage | Fail closed and visibly |
| Context budget | Respect the declared retrieval budget |

The initial executable fixture is intentionally small. It proves the format and gates. Scale, accumulation, and model-based answer-quality datasets will be added without changing the core result contract.

## 9. Metrics

For an ordered result list \(R_k\) and expected relevant set \(G\):

- `precision_at_k` is \(|R_k \cap G| / |R_k|\), or `1.0` when both sets are empty;
- `recall_at_k` is \(|R_k \cap G| / |G|\), or `1.0` when `G` is empty and no result is returned;
- `mrr` is the reciprocal rank of the first relevant item, otherwise `0.0`;
- `ndcg_at_k` uses binary gain and logarithmic discount;
- `policy_violations` counts forbidden IDs returned or forbidden actions allowed;
- `provenance_completeness` is the share of returned items carrying provenance when required;
- `context_tokens` is the adapter's estimate for returned context;
- `latency_ms` is measured around the adapter operation with a monotonic clock.

Aggregate results MUST include case counts and mean quality metrics. Latency aggregates SHOULD include p50 and p95. Future capacity runs SHOULD record ingestion rate, index/storage growth, and latency as the memory set grows.

Metric thresholds are attached to cases or conformance profiles. Missing metrics MUST NOT silently become zero or one.

## 10. Conformance

A result conforms to a profile only when:

1. every required case ran;
2. every security gate passed;
3. no forbidden result or action occurred;
4. all declared minimum thresholds passed;
5. the result document validates against the result schema;
6. suite and dataset hashes match the tested content;
7. the adapter reports its name and version;
8. the run records all required reproducibility metadata.

Skipped cases MUST be listed with a reason. A report MAY compare partial provider capabilities, but it MUST say `conformant: false` if required cases were skipped.

## 11. Result format

The result artifact is JSON validated by `packages/benchmark/schemas/result.schema.json`. It contains:

- schema and suite identity;
- suite SHA-256;
- provider and adapter identity;
- redacted configuration fingerprint;
- source revision and dirty-worktree flag;
- runtime and platform metadata;
- seed and timestamps;
- case-level operation outcomes and metrics;
- aggregate metrics;
- skipped cases;
- disqualifying failures;
- conformance status;
- a deterministic outcome digest excluding clocks and machine-dependent latency.

Published reports MUST retain the raw JSON artifact. Human-readable summaries may be derived from it.

## 12. Hindsight evaluation boundary

The Hindsight adapter maps retain and recall to Hindsight's bank API. The runner creates or uses an isolated benchmark bank ID and sends Chronicle fixture IDs as adapter metadata where the provider permits it.

The adapter does not claim that Hindsight enforces Chronicle authorization, promotion, or Git/OKF policy. Those controls live at the Chronicle gateway. Hindsight results are therefore valid for `provider-retrieval`, not `chronicle-gateway`, until the gateway adapter exists.

Live runs MUST use a disposable bank or an explicit opt-in bank ID. They MUST NOT run against production data. Authentication values MUST come from environment variables and MUST NOT be written to results.

## 13. Reproducibility and publication

Comparable runs SHOULD use:

- the same fixture file and SHA-256;
- the same adapter and provider version;
- an explicit seed;
- an equivalent model configuration;
- a documented warm-up policy;
- at least five measured repetitions for latency claims;
- hardware and runtime metadata;
- a clean source revision.

Deterministic contract runs MUST produce the same outcome digest on repeated execution. Raw latency may differ and is excluded from that digest.

No result may be described as a Chronicle production-readiness certification. Benchmark conformance is evidence for a bounded profile and version.

## 14. Exit codes

The command-line runner uses:

| Code | Meaning |
| --- | --- |
| `0` | All required cases and gates passed |
| `1` | Invalid input, configuration, or runner error |
| `2` | Benchmark completed but did not conform |

## 15. Change control

Breaking changes to fixture or result semantics require a new `schema_version`. Changes to expected outcomes require a new `dataset_version`. Metric corrections require a changelog entry and regenerated baselines.

Changes that weaken a security gate require an RFC and threat-model review.

## 16. Initial acceptance criteria

Version 0.1 is complete when:

- the deterministic adapter passes the committed contract fixture;
- every metric has unit tests, including empty-set behavior;
- a deliberately leaking adapter fails a security gate;
- a repeated deterministic run has the same outcome digest;
- the Hindsight adapter has request/response parsing tests without network access;
- CI runs unit tests, the contract fixture, and repository policy checks;
- the generated result validates against the committed result schema.
