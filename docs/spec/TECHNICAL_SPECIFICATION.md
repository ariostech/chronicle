# Chronicle Technical Specification

**Project:** Chronicle
**Document:** Technical Specification
**Version:** 0.1-draft
**Status:** Draft for implementation
**Date:** 2026-09-11
**Steward:** Arios Technologies

---

## 1. Status and intent

This document defines Chronicle's initial technical contract.

The Project Charter explains what Chronicle is trying to become. This specification defines the concepts, invariants, data boundaries, interfaces, lifecycle rules, and service responsibilities needed to build the first implementation without tying the project to a particular memory engine or model vendor.

This is a pre-1.0 specification. Some details will change as the proof of concept is benchmarked and security-tested. The parts marked **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are intended to be treated as normative requirements for the first implementation unless superseded by an accepted RFC or ADR.

The key architectural rule is simple:

> Chronicle owns the organizational memory contract. Providers such as Hindsight implement part of that contract; they do not define it.

---

## 2. Design vocabulary

Chronicle uses the following terms deliberately.

### 2.1 Principal

An authenticated identity that can perform an operation.

A principal may represent:

- a human user;
- an AI agent;
- an application;
- a service;
- a workload;
- an automation.

A principal MUST have a stable Chronicle identifier even if the upstream identity provider changes.

Example:

```text
principal:user:7d14...
principal:agent:claude-code:...
principal:service:indexer:...
```

### 2.2 Actor

The principal that actually performed an action.

An actor is recorded in audit and provenance metadata.

A principal acting on behalf of another principal MUST NOT erase that distinction.

Example:

```text
resource_owner = principal:user:123
actor          = principal:agent:claude-code:456
```

### 2.3 Source

The original or authoritative material from which a memory, observation, or knowledge item is derived.

Examples:

- an OKF document;
- a Git commit;
- a chat message;
- an issue;
- a meeting transcript;
- a database row;
- a tool result;
- an API response;
- an agent action;
- another memory item.

A source is evidence. A source is not automatically authoritative.

### 2.4 Evidence

A stable reference to material that supports a claim.

Evidence SHOULD retain enough information to reconstruct or re-fetch the source where policy permits.

Evidence MAY contain an immutable snapshot, content hash, source URI, source-system identifier, or a combination.

### 2.5 Memory

A persistent machine-oriented record retained because Chronicle believes it may be useful in a future context.

Memory is not synonymous with chat history.

A memory MUST be scoped and MUST carry provenance.

### 2.6 Episode

A time-bounded experience or event.

Examples:

- a conversation turn;
- an agent attempt;
- an incident;
- a tool execution;
- a decision-making interaction.

Episodes are primarily experiential memory.

### 2.7 Fact

A discrete claim represented in a form Chronicle can retrieve or reason over.

A fact MUST carry an epistemic status and provenance. A fact MAY be wrong, disputed, superseded, or low-confidence.

Chronicle MUST NOT equate "stored fact" with "organizational truth."

### 2.8 Observation

A derived conclusion or pattern synthesized from one or more memories or sources.

An observation MUST identify the evidence or memories that support it.

An observation MUST NOT automatically become institutional knowledge.

### 2.9 Institutional knowledge

Human-readable, organizationally maintained knowledge stored using OKF-compatible Markdown.

Examples:

- decisions;
- runbooks;
- procedures;
- lessons learned;
- policies;
- architecture records;
- project knowledge;
- standards.

Institutional knowledge is version-controlled and intended to be understandable without Chronicle's database.

### 2.10 Candidate knowledge

A proposed institutional-knowledge change that has not yet passed the required review or approval process.

Candidate knowledge MUST be distinguishable from approved institutional knowledge.

### 2.11 Authoritative data

Current operational truth owned by a system of record.

Examples include live balances, inventory, employee status, CRM state, production configuration, and other fast-changing operational values.

Chronicle MUST prefer a live authoritative query when current operational truth is required.

### 2.12 Context

A bounded package of information assembled for a user, agent, or application to perform a task.

Context MAY contain:

- current task state;
- institutional knowledge;
- machine memory;
- live source-system data;
- policies;
- recent events.

Context is not itself a durable memory type.

---

## 3. Core invariants

The implementation MUST preserve these invariants.

### 3.1 Authorization before disclosure

No memory, knowledge item, source-derived text, metadata, title, entity name, result count, or generated summary may be returned if doing so would reveal information outside the caller's effective permissions.

Authorization MUST be enforced before context reaches the model whenever practical.

Post-generation filtering is defense in depth, not the primary control.

### 3.2 Authorization before write

A principal MUST be authorized for the target scope and operation before Chronicle persists a write.

Agents MUST NOT be able to promote their own authority by writing to a broader scope.

### 3.3 Provenance is not optional

Every durable memory and every machine-generated knowledge proposal MUST carry provenance.

Chronicle MUST be able to answer, at minimum:

- who or what created this;
- when Chronicle learned it;
- what source or prior memory supports it.

### 3.4 Machine memory is not institutional truth

Machine-derived memories and observations MUST NOT silently become stable institutional knowledge.

Promotion MUST be an explicit lifecycle transition.

### 3.5 Live systems remain authoritative where designated

Chronicle MUST NOT silently substitute stale memory for a source of record when a policy marks that source as authoritative for current state.

### 3.6 Temporal history is preserved where retention permits

Superseding a fact SHOULD NOT destroy the old fact.

The old fact SHOULD remain available for historical queries, audit, and explanation unless retention or deletion policy requires removal.

### 3.7 Canonical human knowledge is portable

Institutional knowledge MUST remain usable as OKF-compatible Markdown in Git without requiring Chronicle, Obsidian, Hindsight, or the original model provider.

### 3.8 Provider boundaries are explicit

Provider-specific identifiers and internal representations MUST NOT leak into Chronicle's public contract unless explicitly namespaced as provider metadata.

### 3.9 Derived indexes are rebuildable

Search indexes, embeddings, caches, and derived graph projections SHOULD be treated as rebuildable materializations rather than canonical institutional knowledge.

---

## 4. Layer model

Chronicle defines four logical layers.

### 4.1 Working-context layer

Ephemeral state needed by an active task or session.

Chronicle MAY assist with context assembly but SHOULD avoid persisting transient material unless it qualifies for durable memory.

### 4.2 Machine-memory layer

Stores episodes, facts, observations, entity relationships, user preferences, and other machine-oriented retained context.

Hindsight is the initial provider for this layer.

### 4.3 Institutional-knowledge layer

Stores OKF-compatible Markdown under Git version control.

This layer is intended for human inspection, review, and maintenance.

### 4.4 Systems-of-record layer

External systems that remain authoritative for designated operational facts.

Chronicle integrates with these systems but does not attempt to replace them.

---

## 5. Memory types

Chronicle's public model SHOULD support the following initial memory types.

```text
episode
fact
preference
decision_context
task_state
observation
lesson_candidate
procedure_context
entity_note
agent_experience
user_context
project_context
```

The set is extensible.

Unknown memory types MUST NOT automatically be rejected if the enclosing record remains structurally valid and policy-safe.

Providers MAY map several Chronicle memory types to the same internal storage representation.

---

## 6. Epistemic status

Every fact-like memory MUST identify how the claim should be interpreted.

Initial statuses:

```text
observed
asserted
inferred
derived
verified
disputed
unknown
```

### observed

Directly obtained from an event or source.

### asserted

Stated by a user, agent, document, or external source without independent verification.

### inferred

Derived by reasoning beyond what the source explicitly says.

### derived

Computed or summarized deterministically or through a controlled transformation.

### verified

Confirmed through an approved verification mechanism.

### disputed

Known to have conflicting evidence or an active challenge.

### unknown

Used only when imported data cannot yet be classified.

`unknown` SHOULD reduce retrieval authority.

---

## 7. Authority model

Chronicle separates confidence from authority.

Confidence answers:

> How certain is Chronicle that this claim is correct?

Authority answers:

> If claims conflict, how much institutional weight should this source have?

Initial authority classes:

```text
system_of_record
approved_policy
approved_knowledge
approved_decision
verified_memory
user_assertion
external_assertion
agent_observation
agent_inference
unknown
```

Authority SHOULD be configurable by deployment.

A newer low-authority memory MUST NOT automatically supersede a higher-authority current fact.

---

## 8. Confidence model

Confidence MUST NOT be used as a fake probability unless the producing system has a calibrated probabilistic interpretation.

The initial Chronicle contract supports:

```text
high
medium
low
unknown
```

Providers MAY preserve numeric scores as provider metadata.

Chronicle's public behavior SHOULD rely on categorical confidence until a calibrated model is available.

---

## 9. Scope model

Chronicle scope identifies the organizational context in which a resource is visible and meaningful.

Initial scope dimensions:

```text
organization
department
team
project
user
agent
application
session
```

A memory MAY have more than one scope dimension.

Example:

```yaml
scope:
  organization: org:acme
  team: team:platform
  project: project:chronicle
```

### 9.1 Scope does not imply authority

An organization-scoped item is not automatically more authoritative than a project-scoped item.

### 9.2 Scope does not replace policy

Scope narrows the candidate security boundary. Authorization policy decides whether a caller may act on the resource.

### 9.3 Scope inheritance

Chronicle MAY support hierarchical inheritance, but inheritance MUST be explicit in the policy model.

The first implementation MUST NOT assume that membership in a parent scope automatically grants access to every child scope.

### 9.4 Hard and soft boundaries

Chronicle distinguishes:

- **hard boundaries**, which prevent unauthorized storage or retrieval across security domains;
- **soft retrieval partitions**, which improve relevance inside an authorized boundary.

Provider banks, repositories, databases, tenants, or namespaces MAY be used as hard boundaries.

Tags MUST NOT be the sole control for highly sensitive separation.

---

## 10. Principal and authorization model

Chronicle SHOULD integrate with standard identity providers through OIDC/OAuth-capable infrastructure.

The initial authorization model MUST support relationships among:

```text
principal
organization
department
team
project
resource
role
permission
```

Initial permissions:

```text
memory.read
memory.write
memory.correct
memory.delete
memory.reflect

knowledge.read
knowledge.propose
knowledge.review
knowledge.approve
knowledge.retire

evidence.read

scope.read
scope.admin

policy.read
policy.manage

audit.read

provider.admin
system.admin
```

### 10.1 Delegated agents

An agent operating on behalf of a user MUST be distinguishable from the user.

Effective authorization SHOULD be the intersection of:

```text
user authority
∩
agent authority
∩
application/workload authority
∩
resource policy
```

An agent MUST NOT gain access merely because the user has access if the agent itself is restricted.

### 10.2 MCP authorization

For remote HTTP-based MCP access, Chronicle SHOULD follow the current MCP authorization specification and act as a protected resource server or sit behind one.

Access tokens MUST be scoped to Chronicle as the intended resource and MUST NOT be accepted for unrelated downstream systems.

### 10.3 Local/STDIO MCP

Local STDIO integrations MAY use environment-provided credentials or local workload identity.

Local execution MUST NOT be treated as inherently trusted.

---

## 11. Provenance model

Every durable memory MUST include a provenance envelope.

Conceptual structure:

```yaml
provenance:
  actor: principal:agent:...
  created_at: 2026-09-11T16:00:00Z
  method: extracted
  model:
    provider: local
    name: example-model
    version: optional
  sources:
    - source_id: source:...
      locator: optional
      content_hash: optional
      observed_at: 2026-09-11T15:58:00Z
```

### 11.1 Provenance methods

Initial values:

```text
manual
imported
extracted
summarized
inferred
consolidated
computed
promoted
synchronized
```

### 11.2 Transformation chains

When one artifact is derived from another, Chronicle SHOULD preserve the transformation chain rather than replacing the original provenance.

Example:

```text
meeting transcript
  → extracted fact
  → consolidated observation
  → proposed lesson
  → approved OKF knowledge
```

### 11.3 Content hashes

Where the source is stable enough to hash, Chronicle SHOULD store a cryptographic content hash to help establish what content was actually used.

---

## 12. Temporal model

Chronicle needs to distinguish multiple notions of time.

Each durable record SHOULD support:

```text
created_at
observed_at
valid_from
valid_until
superseded_at
archived_at
deleted_at
```

### 12.1 Recorded time

`created_at` means when Chronicle persisted the record.

### 12.2 Observed time

`observed_at` means when the source event occurred or was observed.

### 12.3 Valid time

`valid_from` and `valid_until` describe when the claim is or was considered true.

### 12.4 Supersession

A new claim MAY supersede an older claim without deleting it.

The superseding relation MUST be represented explicitly.

### 12.5 Historical queries

The retrieval contract SHOULD eventually support questions such as:

- what is true now;
- what was believed on a given date;
- what changed between two dates;
- what superseded a particular claim.

---

## 13. Memory lifecycle

Initial memory lifecycle states:

```text
candidate
active
disputed
superseded
archived
expired
deleted
```

### candidate

Extracted or proposed but not yet accepted for normal retrieval.

### active

Eligible for retrieval under policy.

### disputed

Has unresolved conflicting evidence or an explicit challenge.

### superseded

Retained historically but no longer preferred as current context.

### archived

Retained but excluded from normal retrieval unless explicitly requested.

### expired

Outside its retention or TTL window.

### deleted

Logically removed. Physical deletion behavior is controlled by retention and legal-hold policy.

---

## 14. Memory creation pipeline

The default creation path SHOULD be:

```text
event/source
   ↓
candidate detection
   ↓
sensitivity and secret screening
   ↓
classification
   ↓
scope resolution
   ↓
authority assignment
   ↓
entity resolution
   ↓
deduplication/conflict check
   ↓
provider write
   ↓
index/materialization
   ↓
audit event
```

### 14.1 Selective capture

Chronicle SHOULD NOT persist every interaction by default.

Capture policy MAY use:

- explicit "remember" requests;
- deterministic rules;
- provider extraction;
- model-based extraction;
- event type;
- source authority;
- novelty;
- expected future utility.

### 14.2 Secret and sensitive-content screening

Secrets, API tokens, private keys, credentials, and other prohibited material MUST be screened before durable storage.

Deployments SHOULD be able to define additional data classes that may not enter durable memory.

---

## 15. Conflict and supersession semantics

Chronicle MUST distinguish:

```text
duplicate
update
contradiction
supersession
parallel truth
```

### duplicate

Substantially the same claim with no meaningful new state.

### update

New information refines the existing claim without invalidating its core truth.

### contradiction

Two claims cannot both be true under the same scope and valid-time interval.

### supersession

A newer claim intentionally replaces an older claim for current use.

### parallel truth

Different scopes or time intervals allow apparently conflicting claims to coexist.

Example:

```text
Team A uses PostgreSQL.
Team B uses MySQL.
```

This is not a contradiction.

Conflict resolution MUST consider:

- subject/entity identity;
- predicate/claim type;
- scope;
- valid time;
- source authority;
- verification;
- confidence.

---

## 16. Entity model

Chronicle SHOULD maintain stable entity identifiers separate from display names.

Initial entity types may include:

```text
person
role
team
department
organization
project
system
application
repository
customer
vendor
document
incident
decision
procedure
policy
```

The set is extensible.

Aliases and renamed entities SHOULD map to the same canonical entity when evidence supports the match.

Entity merges MUST be auditable and reversible until confidence is sufficient.

---

## 17. Institutional knowledge and OKF

Chronicle adopts OKF v0.2 as the default human-readable institutional knowledge format.

Chronicle MUST NOT fork OKF's core semantics merely to add organizational metadata.

Instead, Chronicle defines a namespaced profile.

### 17.1 OKF compatibility

A Chronicle institutional-knowledge document MUST remain a valid OKF document.

Chronicle SHOULD preserve upstream fields such as:

```text
type
title
description
resource
tags
sources
generated
verified
status
stale_after
```

where applicable.

### 17.2 Chronicle extension namespace

Chronicle-specific metadata SHOULD be contained under:

```yaml
chronicle:
  ...
```

Example:

```yaml
---
okf_version: "0.2"
type: Decision
title: Adopt Hindsight as the initial memory provider
status: stable

generated:
  by: human:oshane
  at: 2026-09-11T16:00:00Z

verified:
  - by: human:architecture-reviewer
    at: 2026-09-11T17:00:00Z

sources:
  - id: memory-evaluation
    resource: ./references/memory-evaluation.md

chronicle:
  id: decision:architecture:0003

  scope:
    organization: org:example
    team: team:platform

  authority: approved_decision
  classification: internal

  owners:
    - team:platform

  valid_from: 2026-09-11T17:00:00Z

  supersedes: []

  retention:
    policy: durable
---
```

### 17.3 Chronicle profile fields

Initial Chronicle profile fields:

```text
id
scope
authority
classification
owners
valid_from
valid_until
supersedes
retention
source_system
canonical_resource
```

Unknown extension fields SHOULD be preserved when possible.

### 17.4 Repository boundaries

Git/OKF bundle boundaries MAY be used as access-control boundaries.

Chronicle MUST NOT rely on frontmatter alone to protect information after repository access has been granted.

Sensitive knowledge SHOULD be separated into repositories/bundles or server-enforced paths consistent with the deployment's security model.

---

## 18. Institutional knowledge lifecycle

Initial states:

```text
draft
proposed
in_review
stable
superseded
retired
```

Where possible, Chronicle SHOULD map these to OKF's upstream lifecycle semantics rather than introducing redundant fields.

### 18.1 Promotion

Machine-derived content MUST enter the institutional-knowledge layer as a proposal unless policy explicitly permits automatic promotion for a narrowly defined low-risk class.

### 18.2 Human review

Policy MAY require one or more human reviewers.

High-authority knowledge such as policy or security procedure SHOULD require human review by default.

### 18.3 Git workflow

The standard collaborative flow SHOULD be:

```text
proposal
  ↓
branch/commit
  ↓
pull request
  ↓
review
  ↓
merge
  ↓
re-index
  ↓
available as stable knowledge
```

Local single-user deployments MAY commit directly if their policy permits.

---

## 19. Knowledge bundles

A knowledge bundle is a Git-versioned directory tree containing OKF documents and related resources.

Initial conventional structure:

```text
knowledge/
├── index.md
├── log.md
├── organization/
├── teams/
├── projects/
├── systems/
├── decisions/
├── runbooks/
├── incidents/
├── lessons/
└── references/
```

This is a convention, not a mandatory ontology.

Chronicle MUST permit organizations to define domain-specific structures.

---

## 20. Provider abstraction

Chronicle's public memory contract is implemented behind a provider interface.

Conceptual capabilities:

```text
retain
recall
search
reflect
get
correct
forget
timeline
evidence
entities
relationships
health
capabilities
```

Providers MAY expose fewer capabilities.

Chronicle MUST support provider capability discovery.

### 20.1 Provider capability model

Example:

```json
{
  "retain": true,
  "recall": true,
  "reflect": true,
  "graph": true,
  "temporal": true,
  "delete": true,
  "evidence": true
}
```

Chronicle SHOULD degrade gracefully where an optional provider capability is absent.

### 20.2 Initial provider

Hindsight is the initial provider.

Provider-specific banks, IDs, and recall parameters MUST remain inside the Hindsight adapter unless explicitly surfaced as diagnostic metadata.

---

## 21. Provider routing

Chronicle MAY eventually support more than one memory provider.

Routing decisions MAY consider:

- memory type;
- scope;
- data residency;
- provider capability;
- tenant policy;
- latency;
- cost;
- security classification.

The first implementation MAY use a single configured provider while preserving the abstraction.

---

## 22. Retrieval pipeline

Chronicle retrieval SHOULD follow:

```text
authenticated request
      ↓
principal and delegated-identity resolution
      ↓
scope resolution
      ↓
policy authorization
      ↓
query classification
      ↓
authorized-source selection
      ↓
memory retrieval
      ↓
knowledge retrieval
      ↓
optional live-source retrieval
      ↓
candidate fusion
      ↓
authority/temporal filtering
      ↓
reranking
      ↓
context budgeting
      ↓
provenance packaging
      ↓
caller
```

### 22.1 No-retrieval behavior

Chronicle MUST support returning no memory when available memories are irrelevant, stale, unauthorized, or insufficiently trustworthy.

Memory injection is not mandatory on every request.

### 22.2 Current versus historical retrieval

Normal task retrieval SHOULD prefer currently valid material.

Explicit historical requests SHOULD be able to retrieve superseded material where policy permits.

---

## 23. Context assembly

Chronicle's Context Assembler is responsible for producing a bounded context package.

A context package SHOULD contain:

```text
request metadata
principal metadata
selected institutional knowledge
selected machine memory
optional live-source facts
policy/instruction metadata
provenance references
token/size accounting
```

### 23.1 Context budget

Context assembly MUST operate within a configurable budget.

Priority SHOULD generally be:

1. mandatory safety/policy constraints;
2. direct task input;
3. authoritative current knowledge;
4. highly relevant memory;
5. supporting historical context;
6. optional supplementary material.

### 23.2 Diversity

The assembler SHOULD avoid filling the entire context budget with many near-duplicate memories.

### 23.3 Explainability

For each returned contextual item, Chronicle SHOULD preserve an identifier that lets the caller request provenance/evidence later.

---

## 24. Public API principles

Chronicle's public API SHOULD be resource-oriented and stable.

The initial API should separate:

```text
/memory
/knowledge
/context
/evidence
/entities
/scopes
/audit
/providers
```

Exact paths remain implementation decisions until the API specification is generated.

### 24.1 Idempotency

Write operations that may be retried SHOULD support idempotency keys.

### 24.2 Correlation IDs

Every request SHOULD receive a correlation ID propagated into audit, provider calls, and logs.

### 24.3 Pagination

List/search endpoints MUST use deterministic pagination semantics.

### 24.4 Error model

Errors SHOULD include:

```text
code
message
correlation_id
retryable
details
```

Details MUST NOT leak unauthorized resource information.

---

## 25. MCP contract

Chronicle's MCP server SHOULD expose a small semantic surface rather than mirroring every REST endpoint.

Initial candidate tools:

```text
chronicle_context
chronicle_recall
chronicle_remember
chronicle_knowledge_search
chronicle_knowledge_read
chronicle_evidence
chronicle_correct_memory
chronicle_forget_memory
chronicle_propose_knowledge
```

The exact set should be reduced further if the proof of concept shows overlap.

### 25.1 Tool authorization

The tools advertised to an MCP client MAY vary according to the caller's authorized scope.

### 25.2 Side effects

Tools with durable or privileged side effects SHOULD be clearly identified.

Clients SHOULD be able to require human confirmation for high-impact operations.

### 25.3 Agent identity

MCP requests MUST be attributable to both the human/resource owner and the acting agent where applicable.

---

## 26. Systems-of-record integration

A source connector MUST declare whether it represents:

```text
authoritative_live
authoritative_snapshot
reference_only
untrusted_external
```

### 26.1 Live authoritative reads

When a query requires live current state, Chronicle SHOULD query the source rather than relying on old memory.

### 26.2 Caching

Cached authoritative data MUST carry freshness metadata and SHOULD be excluded when stale for the requested use.

### 26.3 ACL propagation

Where a source exposes permissions, Chronicle SHOULD preserve or map those permissions into retrieval policy.

Chronicle MUST NOT intentionally broaden source permissions during ingestion.

---

## 27. Retention model

Every durable resource SHOULD resolve to a retention policy.

Initial policy concepts:

```text
ttl
archive_after
delete_after
retain_until
legal_hold
manual_only
durable
```

### 27.1 Expiry

Expired memory MUST be excluded from normal retrieval.

### 27.2 Deletion propagation

When policy requires deletion, Chronicle SHOULD remove or invalidate the resource across:

- canonical store;
- provider store;
- embeddings/indexes;
- caches;
- derived projections.

Audit metadata MAY be retained if policy allows, but MUST NOT preserve deleted sensitive content.

### 27.3 Institutional knowledge

Git history complicates deletion.

Deployments that require erasure MUST define how sensitive institutional knowledge is kept out of immutable/shared history or how repository rewriting is handled.

---

## 28. Classification model

Initial information classifications:

```text
public
internal
confidential
restricted
```

Deployments MAY define their own classification vocabulary.

Classification is descriptive metadata.

Actual access MUST be enforced by policy.

---

## 29. Audit model

Chronicle MUST produce audit events for security-relevant operations.

Initial event classes:

```text
auth.success
auth.failure

memory.read
memory.write
memory.correct
memory.delete
memory.reflect

knowledge.read
knowledge.propose
knowledge.review
knowledge.approve
knowledge.retire

evidence.read

policy.change
scope.change
provider.change
admin.action
```

Each event SHOULD include:

```text
timestamp
correlation_id
actor
resource_owner, if delegated
operation
resource_type
resource_id
scope
decision
policy_reference
client/application
result
```

Sensitive content SHOULD NOT be copied into audit logs by default.

---

## 30. Observability

Operational telemetry SHOULD include:

```text
request latency
provider latency
retrieval count
retrieval hit rate
retrieval rejection rate
context size
memory writes
knowledge promotions
authorization denials
provider errors
queue depth
index lag
retention jobs
model usage
embedding usage
```

OpenTelemetry SHOULD be the preferred interoperability mechanism.

Telemetry MUST NOT become an accidental copy of sensitive memory.

---

## 31. Async processing

The following operations SHOULD be eligible for background execution:

```text
memory extraction
consolidation
reflection
entity resolution
deduplication
conflict analysis
OKF validation
indexing
re-embedding
knowledge-proposal generation
staleness checks
retention jobs
benchmark evaluation
```

Interactive writes SHOULD acknowledge the durable event before non-essential enrichment is complete where safe.

---

## 32. Event model

Chronicle SHOULD use durable internal events for lifecycle transitions even if the first implementation does not deploy a dedicated event-stream platform.

Examples:

```text
MemoryCandidateCreated
MemoryActivated
MemoryDisputed
MemorySuperseded
MemoryExpired

KnowledgeProposed
KnowledgeReviewed
KnowledgeApproved
KnowledgeSuperseded
KnowledgeRetired

ScopeChanged
PolicyChanged
ProviderFailed
```

A future event bus SHOULD be replaceable without changing public contracts.

---

## 33. Storage model

The initial implementation SHOULD use PostgreSQL for Chronicle's transactional state.

Chronicle SHOULD keep its own database logically separate from Hindsight's provider database even when both use the same PostgreSQL server.

Conceptual Chronicle-owned tables/collections include:

```text
principals
scopes
memberships
policies
resources
provenance
evidence
knowledge_registry
provider_mappings
retention_policies
audit_index
jobs
```

Machine memory content primarily owned by Hindsight SHOULD remain behind the provider interface.

---

## 34. Derived search/index layer

Chronicle MAY build indexes over OKF and other authorized knowledge.

Potential indexes:

```text
full-text
embeddings
entity graph
temporal index
citation graph
```

These MUST be treated as derived.

An index loss SHOULD be recoverable from canonical knowledge and source metadata.

---

## 35. Docker deployment contract

The supported Docker Compose stack is part of the product.

The default development/self-hosted deployment SHOULD include:

```text
chronicle-server
chronicle-worker
chronicle-mcp
hindsight
postgres
```

Where practical, Chronicle services SHOULD use a common Chronicle image with different commands.

### 35.1 Hindsight isolation

Hindsight SHOULD run as a separate container.

Chronicle MUST communicate with it through the provider adapter.

### 35.2 PostgreSQL

A single PostgreSQL service MAY host separate Chronicle and Hindsight databases for the default deployment.

### 35.3 Optional profiles

The project SHOULD support Compose profiles for optional functionality such as:

```text
local-ai
observability
collaboration
development
```

### 35.4 Local AI

A `local-ai` profile SHOULD be able to bring up a supported local model service such as Ollama.

The default core stack SHOULD NOT silently download a large model without user intent.

### 35.5 Bootstrap

First startup SHOULD automate:

1. dependency readiness;
2. Chronicle migrations;
3. provider readiness;
4. initial configuration;
5. local knowledge-bundle initialization;
6. provider namespace/bank initialization;
7. health checks;
8. first-admin setup path.

No documented quickstart should require manual `docker exec` steps for ordinary installation.

### 35.6 Version pinning

Released Compose configurations MUST pin tested dependency versions.

Floating `latest` tags SHOULD NOT be used for production-oriented releases.

---

## 36. Configuration

Configuration SHOULD be possible through environment variables and configuration files.

Secrets MUST NOT be written into Git-tracked configuration examples.

Chronicle SHOULD support secret injection through environment, files, or orchestration-native secret mechanisms.

Configuration MUST distinguish:

```text
runtime configuration
secrets
policy
knowledge
provider configuration
```

These concerns SHOULD NOT be collapsed into one giant environment file long term.

---

## 37. Local-first behavior

Chronicle SHOULD support a useful single-machine deployment without external cloud dependencies.

A local deployment should be able to use:

- local Git;
- local PostgreSQL;
- Hindsight;
- local embeddings/model endpoints;
- local MCP clients;
- Obsidian.

Cloud services MAY improve convenience but MUST NOT be required for the core self-hosted path.

---

## 38. Obsidian integration contract

Obsidian is a client over Chronicle knowledge, not the canonical database.

The plugin SHOULD:

- work with ordinary OKF Markdown;
- preserve normal Obsidian behavior;
- show Chronicle provenance and lifecycle metadata without hiding the underlying file;
- connect to Chronicle for authorized memory/context operations;
- allow knowledge proposals and reviews where policy permits;
- continue to provide useful vault access when Chronicle is offline.

The plugin MUST NOT make the vault unreadable without Chronicle.

---

## 39. Git semantics

Git is the default change-history mechanism for institutional knowledge.

Chronicle SHOULD preserve:

```text
commit identity
commit hash
branch
review/PR reference, where available
file path
content hash
```

in the knowledge registry.

Git history MUST NOT be treated as the sole authorization system.

---

## 40. Security boundaries

The initial threat model MUST treat the following as separate trust boundaries:

```text
human client
agent client
Chronicle Gateway
authorization service
memory provider
model endpoint
Git repository
external source connector
database
MCP transport
```

Crossing any boundary requires explicit authentication, authorization, input validation, or a documented trust assumption.

---

## 41. Prompt-injection and memory-poisoning policy

Retrieved content MUST be treated as data, not as privileged instruction.

Chronicle SHOULD:

- preserve source origin;
- classify external/untrusted content;
- avoid turning retrieved text into system-level instruction;
- allow suspicious memory to be quarantined or disputed;
- prevent low-authority sources from silently overwriting higher-authority knowledge;
- record which memory influenced a result.

Provider-native protections MAY be used, but Chronicle's policy MUST NOT depend solely on a provider prompt.

---

## 42. Secret-handling policy

Chronicle MUST attempt to prevent durable storage of:

```text
passwords
API keys
access tokens
refresh tokens
private keys
session secrets
authentication cookies
```

unless a future explicitly designed secure-secret capability says otherwise.

Secret detection SHOULD occur before provider writes and before knowledge proposals.

---

## 43. Failure semantics

Chronicle SHOULD fail closed for authorization uncertainty.

Examples:

- provider unavailable: return a provider failure, not invented memory;
- authorization unavailable: deny protected retrieval;
- source unavailable: identify freshness/source failure;
- context budget exceeded: return the highest-priority authorized subset;
- OKF parse failure: quarantine or report the document rather than silently misinterpret it.

---

## 44. Provider failure isolation

A provider outage SHOULD NOT make institutional knowledge unreadable.

Likewise, an OKF indexing outage SHOULD NOT destroy provider memory.

The system should degrade by layer rather than failing as one monolith where practical.

---

## 45. Backup and recovery

The first production-ready version MUST document backup and restore for:

```text
Chronicle PostgreSQL
Hindsight/provider persistence
Git/OKF repositories
configuration/policy state
secrets references
```

Derived indexes SHOULD be rebuildable and need not be primary backup artifacts.

Restore procedures MUST be tested before 1.0.

---

## 46. Migration

Database and provider migrations MUST be versioned.

Chronicle SHOULD support:

```text
schema migration
provider mapping migration
knowledge-profile migration
re-indexing
re-embedding
```

Provider replacement SHOULD be possible without rewriting canonical OKF knowledge.

---

## 47. Benchmark contract

Chronicle's provider and retrieval architecture MUST be evaluated using executable tests.

Initial benchmark classes:

```text
fact recall
preference recall
contradiction handling
supersession
historical query
entity aliasing
project isolation
user isolation
agent isolation
unauthorized write
memory poisoning
stale source
knowledge promotion
provenance completeness
provider outage
large-memory retrieval
context-budget quality
deletion propagation
```

Metrics SHOULD include:

```text
precision@k
recall@k
MRR
nDCG
task success
temporal correctness
policy violations
p50/p95 latency
context tokens
storage growth
```

Security failures SHOULD be treated as disqualifying rather than averaged into a performance score.

---

## 48. Compatibility policy

Chronicle pre-1.0 MAY introduce breaking changes, but breaking changes MUST be documented.

Once 1.0 is reached, the project SHOULD provide compatibility guarantees for:

```text
public REST API
MCP tool semantics
provider interface
Chronicle OKF profile
configuration schema
backup/restore format where promised
```

Semantic Versioning SHOULD be used for project releases.

---

## 49. Open-source implementation rules

The implementation SHOULD remain usable without proprietary Arios services.

Core governance, authorization, audit, local deployment, memory-provider abstraction, OKF/Git support, MCP, and local-model support belong in the open-source project.

Optional commercial services MUST integrate through documented public interfaces wherever practical.

---

## 50. Initial component map

The first implementation is expected to contain logical components similar to:

```text
chronicle-server
  authentication hooks
  authorization
  scope service
  memory gateway
  knowledge service
  context assembler
  evidence/provenance service
  audit API

chronicle-worker
  async memory jobs
  consolidation jobs
  indexing
  retention
  knowledge proposals

chronicle-mcp
  MCP server
  identity propagation
  semantic tools

provider-hindsight
  Hindsight adapter
  bank/namespace mapping
  provider capability discovery

knowledge-okf
  parser
  validator
  Chronicle profile
  Git integration
  registry/index hooks
```

These may initially live in one monorepo and one runtime image.

Logical separation does not require immediate microservices.

---

## 51. Initial repository layout

The implementation should start as a monorepo.

Recommended layout:

```text
chronicle/
├── README.md
├── LICENSE
├── NOTICE
├── CHANGELOG.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── SECURITY.md
├── GOVERNANCE.md
├── CODE_OF_CONDUCT.md
│
├── apps/
│   ├── server/
│   ├── admin/
│   └── docs/
│
├── packages/
│   ├── protocol/
│   ├── sdk-typescript/
│   ├── sdk-python/
│   ├── mcp/
│   ├── auth/
│   ├── knowledge-okf/
│   ├── provenance/
│   └── benchmark/
│
├── providers/
│   └── hindsight/
│
├── integrations/
│   ├── obsidian/
│   ├── claude-code/
│   └── opencode/
│
├── deploy/
│   ├── docker/
│   └── compose/
│
├── docs/
│   ├── project/
│   ├── spec/
│   ├── architecture/
│   ├── security/
│   ├── adr/
│   └── rfc/
│
├── examples/
└── tests/
    ├── unit/
    ├── integration/
    ├── e2e/
    └── security/
```

The implementation language and exact package tooling are intentionally not fixed by this document.

---

## 52. MVP API behaviors

The proof of concept MUST demonstrate the following behaviors even if endpoint names differ.

### 52.1 Remember

An authorized principal can submit an event or explicit memory candidate.

Chronicle:

1. authenticates the actor;
2. resolves target scope;
3. authorizes the write;
4. screens content;
5. records provenance;
6. calls the configured memory provider;
7. stores the provider mapping;
8. records audit.

### 52.2 Recall

An authorized principal can request relevant memory.

Chronicle:

1. resolves effective identity;
2. determines authorized scopes;
3. queries only eligible provider partitions;
4. filters for temporal validity and policy;
5. reranks;
6. returns provenance references.

### 52.3 Knowledge search

Chronicle searches only authorized OKF bundles and returns:

```text
document ID
title
type
summary/snippet
status
authority
freshness
source/provenance reference
```

### 52.4 Context request

A client can request a context package for a task with a declared budget.

Chronicle assembles memory, knowledge, and optional live-source context under authorization.

### 52.5 Knowledge proposal

An authorized actor can create a candidate OKF change from a memory/observation.

The proposal records its source evidence and does not become stable knowledge until the required review completes.

### 52.6 Correction

An authorized principal can dispute or correct memory.

Correction SHOULD create a traceable state transition rather than silently rewriting history.

### 52.7 Forget

An authorized principal can request deletion/retirement subject to retention and hold policy.

---

## 53. MVP acceptance scenario

The first milestone is complete only when this works end to end:

1. A user creates or edits an OKF document in an Obsidian-compatible knowledge bundle.
2. The change is committed to Git.
3. Chronicle validates and indexes the document.
4. A fresh coding-agent session authenticates through MCP.
5. Chronicle resolves the user, agent, project, and permitted scopes.
6. The agent retrieves the relevant approved knowledge.
7. The agent performs work and encounters a reusable lesson.
8. Hindsight retains the relevant experience and evidence.
9. A durable observation becomes available.
10. Chronicle creates a candidate OKF change tied to the supporting evidence.
11. A human reviews the Git change.
12. The change is merged and becomes stable institutional knowledge.
13. A later fresh agent session retrieves the approved knowledge.
14. Chronicle can explain where that knowledge came from and what evidence supported its promotion.

---

## 54. Deferred capabilities

The following are intentionally deferred unless the proof of concept requires them:

```text
multi-region federation
cross-organization shared memory
custom graph database
HelixDB production dependency
provider ensembles
automatic high-authority promotion
advanced policy UI
full enterprise connector catalog
mobile client
custom document editor
reinforcement-learned memory management
```

Deferral is deliberate. It prevents the project from becoming infrastructure-heavy before the memory/knowledge lifecycle is proven.

---

## 55. Required follow-on specifications

This document is intentionally broad enough to stabilize implementation direction without pretending every subsystem is fully designed.

Before production hardening, Chronicle should add:

```text
docs/architecture/REFERENCE_ARCHITECTURE.md
docs/security/THREAT_MODEL.md
docs/spec/API.md
docs/spec/MCP.md
docs/spec/OKF_PROFILE.md
docs/spec/AUTHORIZATION.md
docs/spec/PROVIDER_INTERFACE.md
docs/spec/BENCHMARK.md
```

Each follow-on document should remain consistent with this specification unless an accepted RFC/ADR changes the contract.

---

## 56. Initial implementation questions still open

The following decisions are deliberately unresolved:

- primary implementation language;
- framework choices;
- authorization engine;
- identity-provider integration library;
- job/queue implementation;
- full-text/index implementation for OKF;
- embedding model defaults;
- local LLM defaults;
- exact Hindsight bank/scope mapping;
- repository-per-scope versus bundle-per-scope defaults;
- admin UI framework;
- Git hosting integration strategy;
- exact REST resource paths;
- exact MCP tool set;
- whether Chronicle stores a normalized entity graph independently of Hindsight;
- when HelixDB or another graph/vector store should be introduced.

These should be resolved through ADRs after the reference architecture and threat model make the trade-offs concrete.

---

## 57. External standards and upstream dependencies

Chronicle currently intends to align with:

- Open Knowledge Format (OKF) v0.2 for institutional knowledge;
- Model Context Protocol (MCP) for agent interoperability;
- OAuth/OIDC-compatible identity infrastructure for remote authenticated access;
- Git for institutional-knowledge version history;
- Semantic Versioning for Chronicle releases;
- OpenTelemetry for observability interoperability.

Hindsight is an initial implementation dependency, not a Chronicle standard.

---

## 58. Specification change process

Before 1.0, changes to this specification may be made through reviewed pull requests.

Changes that alter any of the following SHOULD use an RFC and ADR:

- trust boundaries;
- public resource semantics;
- authorization semantics;
- authority model;
- memory lifecycle;
- knowledge lifecycle;
- provider interface;
- OKF profile compatibility;
- MCP behavior;
- deletion/retention guarantees.

Implementation details that preserve the contract do not require an RFC.

---

## 59. Definition of done for Technical Specification v0.1

This specification is ready to move into reference architecture work when maintainers agree that it answers these questions:

- What is memory in Chronicle?
- What is institutional knowledge?
- What remains authoritative outside Chronicle?
- Who or what is acting?
- How is scope represented?
- How is authorization enforced?
- How are authority and confidence different?
- How is provenance retained?
- How is time represented?
- How are contradictions and supersession handled?
- How does machine memory become candidate knowledge?
- How does candidate knowledge become approved knowledge?
- What does the memory-provider boundary look like?
- What does an agent retrieve?
- What belongs in the default Docker stack?
- What is explicitly deferred?

If those answers are stable enough to implement and test, the next artifact is the Reference Architecture.

---

## 60. Closing rule

Chronicle should never require a user to trust an opaque memory simply because an AI system stored it.

A useful memory system must be able to preserve context.

An organizational memory system must also preserve boundaries, history, provenance, authority, and the ability for people to inspect and correct what the organization is carrying forward.
