# Chronicle Security and Threat Model

**Project:** Chronicle
**Document:** Security and Threat Model
**Version:** 0.1-draft
**Status:** Draft for implementation
**Date:** 2026-09-11
**Steward:** Arios Technologies

---

## 1. Purpose

Chronicle sits between people, AI agents, memory providers, institutional knowledge, and systems of record. That position makes it a security boundary, not just a retrieval service.

This document identifies the assets Chronicle must protect, the actors that interact with them, the trust boundaries created by the reference architecture, the threats that arise at those boundaries, and the controls the implementation should require before production use.

The threat model is intentionally written before implementation choices such as the authorization engine, queue, model provider, or hosted deployment pattern are finalized. Those choices should be constrained by the threat model rather than documented after the fact.

---

## 2. Scope

This threat model covers:

- Chronicle Gateway/API;
- MCP server;
- background workers;
- Hindsight integration and the provider abstraction;
- PostgreSQL;
- Git repositories containing OKF institutional knowledge;
- Obsidian integration;
- coding-agent integrations such as Claude Code and OpenCode;
- local and hosted model endpoints;
- systems-of-record connectors;
- source ingestion;
- audit and provenance services;
- Docker Compose deployment;
- future administrative surfaces.

External systems are considered at the boundary where Chronicle interacts with them. This document does not attempt to fully threat-model every external product.

---

## 3. Security goals

Chronicle should protect five properties.

### Confidentiality

Information must not be disclosed outside the principal, scope, tenant, project, or policy boundary that governs it.

### Integrity

Memory, institutional knowledge, provenance, policy, and audit data must not be changed by unauthorized actors.

### Availability

Authorized users and agents should be able to retrieve required context without one optional subsystem causing the entire platform to fail.

### Accountability

Important reads, writes, promotions, deletions, policy changes, and privileged operations should be attributable to a concrete actor.

### Epistemic integrity

Chronicle must preserve the distinction between:

- what was observed;
- what was asserted;
- what was inferred;
- what was verified;
- what has been approved as institutional knowledge;
- what a system of record currently says.

This last property is specific to Chronicle's purpose. A technically secure system that allows untrusted memories to become organizational truth without traceability would still fail Chronicle's security model.

---

## 4. Security principles

### 4.1 Authorize before disclosure

Chronicle must constrain candidate sources before sensitive data enters model context where practical. Post-generation filtering is defense in depth, not the primary control.

### 4.2 Authorize before durable writes

Writing shared memory is privileged. An agent that cannot read a team scope must not be able to write into that team scope.

### 4.3 Agents are separate security principals

An AI agent operating for a user is not identical to the user. Chronicle must retain both identities during delegated work.

### 4.4 Models do not decide access

A language model must never decide whether a caller is authorized to read a memory, retrieve a document, or perform a privileged operation. Models may help with classification or relevance only after enforceable security decisions have constrained the candidate set.

### 4.5 Retrieved content is data, not instruction

Content from memory, documents, websites, tickets, repositories, APIs, and other MCP servers must be treated as untrusted data unless explicitly designated otherwise. A retrieved instruction does not gain authority merely because it appears in context.

### 4.6 Provenance is security metadata

The provenance chain must be protected from tampering with the same seriousness as the memory itself. If an attacker can rewrite origin or evidence, they can change how much the organization trusts a claim.

### 4.7 Fail closed when trust cannot be resolved

If Chronicle cannot safely resolve identity, scope, policy, source permissions, or freshness, protected access should fail closed.

### 4.8 Canonical and derived state are different

Search indexes, embeddings, caches, and graph projections are derived. They must not become an ungoverned route around the policy enforced on canonical sources.

### 4.9 Security belongs in the open-source core

Authorization, audit, retention, secure self-hosting, and export controls are part of Chronicle's core product, not enterprise-only additions.

---

## 5. Assets

Chronicle protects several classes of assets.

### 5.1 Machine memory

Examples:

- agent experiences;
- project events;
- user preferences;
- observations;
- entity relationships;
- failure patterns;
- prior actions;
- task context.

Primary risks:

- unauthorized disclosure;
- poisoning;
- unauthorized alteration;
- hidden persistence;
- incorrect scope;
- stale retrieval;
- deletion failure.

### 5.2 Institutional knowledge

Examples:

- decisions;
- policies;
- runbooks;
- lessons;
- architecture notes;
- system documentation;
- project knowledge.

Primary risks:

- unauthorized Git access;
- malicious changes;
- secret commits;
- forged approval;
- stale approved content;
- compromised history;
- unsafe promotion from memory.

### 5.3 Provenance and evidence

Examples:

- source references;
- content hashes;
- transformation chains;
- actor identity;
- source timestamps;
- verification records.

Primary risks:

- tampering;
- omission;
- forged origin;
- broken chain;
- source substitution.

### 5.4 Authorization and scope state

Examples:

- memberships;
- project/team relationships;
- policy assignments;
- role bindings;
- agent delegation;
- provider namespace mapping.

Primary risks:

- privilege escalation;
- stale permissions;
- confused-deputy access;
- incorrect inheritance.

### 5.5 Audit data

Examples:

- reads;
- writes;
- policy changes;
- knowledge approval;
- deletion;
- provider changes.

Primary risks:

- tampering;
- deletion;
- sensitive-content leakage through logs;
- incomplete attribution.

### 5.6 Credentials and secrets

Examples:

- database credentials;
- API keys;
- OAuth tokens;
- model-provider credentials;
- Git credentials;
- MCP credentials.

Primary risks include accidental storage in memory, logs, Markdown, Git history, model context, or container environment output.

### 5.7 Availability and capacity

Examples:

- model quota;
- storage;
- worker capacity;
- database connections;
- provider throughput.

Primary risks:

- denial of service;
- cost exhaustion;
- unbounded memory growth;
- recursive agent behavior;
- oversized context requests.

---

## 6. Actors

### Authorized human user

A legitimate user operating within assigned scopes. Risk can still arise from mistakes, unsafe sharing, compromised credentials, or misuse.

### Knowledge owner or reviewer

A user allowed to review or approve institutional knowledge. This is a higher-impact role because approval can change organizational authority.

### Administrator

A principal that can change configuration, scopes, policies, providers, or identity mappings.

### AI agent

A delegated or autonomous actor such as Claude Code, OpenCode, an internal assistant, or a workflow agent.

### Service or workload

A non-human component such as a worker, indexer, Git synchronizer, connector, or scheduled job.

### External source

A system that provides data but is not fully trusted by Chronicle, including websites, documents, issue trackers, repositories, or external MCP servers.

### External model endpoint

A local or hosted model service. Approval to use a model endpoint does not make its output authoritative.

### Memory provider

Initially Hindsight. The provider is trusted to perform configured memory functions but is not Chronicle's authorization authority.

### Malicious outsider

An attacker without legitimate Chronicle access.

### Malicious insider

An authenticated person intentionally abusing granted access.

### Compromised principal

A user, service, or agent whose credentials or execution environment have been taken over.

---

## 7. Trust boundaries

Chronicle's reference architecture creates these primary boundaries:

```text
Human client
    |
    v
Chronicle Gateway
    |
    +--> authorization/policy
    +--> Hindsight
    +--> Git / OKF
    +--> PostgreSQL
    +--> model endpoint
    +--> systems of record
    +--> MCP / agent clients
```

Each crossing is a security decision.

### Boundary A — Human client to Chronicle

Threats include stolen credentials, malformed requests, malicious uploads, session abuse, and over-broad user privileges.

### Boundary B — Agent to Chronicle

Threats include prompt injection, compromised agent runtimes, excessive agency, replay, confused-deputy behavior, and tool abuse.

### Boundary C — Chronicle to Hindsight

Threats include namespace mapping errors, provider leakage, provider compromise, unsafe provider-side prompt use, and accidental bypass of Chronicle policy.

### Boundary D — Chronicle to Git/OKF

Threats include unauthorized commits, malicious Markdown, poisoned proposals, approval forgery, and secrets preserved in history.

### Boundary E — Chronicle to model endpoint

Threats include data exfiltration, prompt leakage, model-provider compromise, untrusted output, and external provider logging.

### Boundary F — Chronicle to system of record

Threats include over-privileged credentials, ACL mismatch, stale mirrored permissions, and unsafe writes if connectors later support mutation.

### Boundary G — External source to Chronicle

Threats include indirect prompt injection, poisoned content, misleading provenance, malformed data, and hostile payloads.

### Boundary H — Chronicle to PostgreSQL

Threats include SQL injection, over-privileged DB roles, backup exposure, and unauthorized direct access.

### Boundary I — Container host to workloads

Threats include host compromise, container escape, secret leakage, excessive Linux capabilities, and unsafe writable mounts.

---

## 8. Threat taxonomy

Chronicle should use conventional threat-modeling concepts alongside AI/agent-specific risks.

Primary categories include:

```text
spoofing
tampering
repudiation
information disclosure
denial of service
elevation of privilege

prompt injection
indirect prompt injection
memory poisoning
retrieval poisoning
excessive agency
tool misuse
confused deputy
model output misuse
sensitive information disclosure
unbounded consumption
supply-chain compromise
knowledge-promotion abuse
provenance forgery
temporal manipulation
scope contamination
```

---

## 9. P0: Cross-scope information disclosure

### Scenario

A user or agent authorized for Project A retrieves information belonging to Project B.

Possible causes include:

- incorrect provider filters;
- wrong Hindsight bank mapping;
- a derived index containing multiple security domains;
- filtering after retrieval rather than before it;
- global embedding search;
- cache reuse across principals.

### Impact

Critical. Chronicle's core promise depends on shared memory without shared exposure.

### Required controls

- explicit authorized-scope list;
- hard provider partitions where required;
- per-resource authorization as defense in depth;
- security-aware cache keys;
- security metadata on derived indexes;
- automated isolation tests;
- no global retrieval followed only by prompt instructions to ignore unauthorized items.

### Required tests

- cross-user retrieval;
- cross-project retrieval;
- cross-team retrieval;
- cache isolation;
- invalid provider tag;
- missing scope metadata;
- mixed-authority search indexes.

---

## 10. P0: Unauthorized shared-memory write

### Scenario

An agent with user-level or project-level access writes false or malicious information into a team or organization scope.

### Impact

Critical. Shared memory poisoning can influence future users and agents long after the original session ends.

### Controls

- authorize target scope before provider write;
- separate read and write permissions;
- explicit actor identity;
- restricted agent write scopes;
- provider namespaces not selectable directly by untrusted clients;
- candidate state for risky memory types;
- audit shared-scope writes;
- rate-limit durable writes.

---

## 11. P0: Memory poisoning

### Scenario

An attacker causes Chronicle to retain misleading instructions or facts designed to alter future agent behavior.

Possible sources include hostile websites, poisoned documents, malicious issues, compromised users, malicious agents, or external MCP output.

### Attack path

```text
hostile source
  -> ingestion
  -> durable memory
  -> later recall
  -> agent context
  -> tool use or data disclosure
```

### Controls

- retrieved content is tagged as data;
- source authority is preserved;
- memory extraction separates claims from instructions;
- suspicious directives from untrusted sources do not become trusted instruction;
- source origin survives consolidation;
- candidate/quarantine states are available;
- high-impact promotion requires review;
- repeated text does not automatically increase authority.

---

## 12. P0: Indirect prompt injection

Chronicle is especially exposed to indirect prompt injection because its purpose is to ingest and recall external content.

OWASP guidance treats prompt injection as a primary LLM-system risk and explicitly notes that retrieval/RAG does not inherently solve it.

### Controls

- content/source trust labels;
- strict separation of instruction channels and data channels;
- tool authorization independent of model output;
- confirmation or policy gates for high-impact actions;
- provenance visible to the agent/runtime;
- low-authority external content cannot become system instruction;
- the context assembler may exclude instruction-like content where the use case does not require it.

---

## 13. P0: Knowledge-promotion abuse

### Scenario

A malicious or compromised agent converts false memory into an OKF change and causes it to become approved institutional knowledge.

Attack paths include automatic merge, forged reviewer identity, compromised Git credentials, review fatigue, PR spam, or an ambiguous source chain.

### Controls

- machine-generated proposals are clearly marked;
- provenance is attached to proposals;
- human review is required for high-authority knowledge;
- branch protection;
- reviewer authorization;
- approval policy varies by knowledge type;
- no automatic promotion of policy/security decisions;
- proposal rate limiting and deduplication;
- review UI exposes evidence.

---

## 14. P0: Confused-deputy access through agents

### Scenario

A user has access to Finance and Engineering. A coding agent should only operate on Engineering Project X. If Chronicle authorizes only the user and ignores the acting agent, the coding agent may receive Finance data.

### Required model

Effective authorization should be the intersection of:

```text
human principal
∩ agent principal
∩ application/workload
∩ delegated project/scope
∩ target resource policy
```

Chronicle must retain all relevant identities during the request.

---

## 15. P0: Provenance forgery

### Scenario

A memory is presented as originating from an authoritative source when it actually came from an untrusted source or model inference.

### Controls

- provenance generated by trusted server-side components;
- clients cannot assign high-authority classes arbitrarily;
- stable source IDs;
- content hashes where practical;
- provider metadata separated from Chronicle provenance;
- transformation history is append-oriented;
- provenance changes are audited.

---

## 16. P1: MCP authorization failure

Current MCP specifications place significant emphasis on authorization hardening. Chronicle's remote MCP deployment must treat MCP as a protected resource rather than as a trusted local extension by default.

Threats include:

- token audience confusion;
- authorization-server mix-up;
- bearer-token replay;
- over-broad scopes;
- client impersonation;
- tool invocation outside delegated authority.

### Controls

- validate token resource/audience;
- validate authorization issuer where applicable;
- use short-lived tokens;
- least-privilege scopes;
- TLS for remote MCP;
- separate MCP identity from downstream credentials;
- never pass Chronicle access tokens through to unrelated downstream systems;
- define a trust model even for local STDIO integrations.

---

## 17. P1: Sensitive information disclosure through model context

### Scenario

Chronicle sends confidential memory to a hosted model endpoint not approved for that classification.

### Controls

- classification-aware model routing;
- policies such as `local_only` and `approved_remote`;
- egress controls;
- send only necessary context;
- document external-provider data handling;
- audit which model route handled sensitive requests.

---

## 18. P0: Secret ingestion

### Scenario

A user pastes credentials into a conversation or an agent reads a `.env` file. Chronicle extracts the secret and persists it as memory or knowledge.

### Controls

Pre-storage screening should cover:

- passwords;
- API keys;
- private keys;
- access tokens;
- refresh tokens;
- authentication cookies;
- connection strings where appropriate.

Additional controls:

- Git pre-commit or server-side secret scanning;
- never log secret values;
- configurable deny patterns;
- deletion workflow for accidental persistence;
- explicit documentation that Git history may retain committed secrets.

---

## 19. P1: Stale authorization

### Scenario

A user's team membership is revoked, but cached policy continues to permit access.

### Controls

- bounded authorization-cache TTL;
- event-driven invalidation where available;
- sensitive scopes use shorter cache lifetimes;
- authorization decisions carry policy version;
- privilege changes invalidate active sessions/tokens where possible.

---

## 20. P1: Stale memory presented as current truth

### Scenario

Chronicle recalls an old CRM status and presents it as current even though the source system changed.

### Controls

- valid-time metadata;
- authority markers;
- source designations such as `authoritative_live`;
- query live sources when current state is required;
- stale memory is labeled;
- context assembly favors current authoritative state.

---

## 21. P1: Temporal manipulation

### Scenario

An attacker changes timestamps or validity ranges so an old fact appears current.

### Controls

- server-generated ingestion timestamps;
- source timestamps stored separately;
- validity changes are audited;
- clients cannot backdate high-authority state without permission;
- supersession is explicit.

---

## 22. P1: Malicious Git/OKF content

Markdown is human-readable, but that does not make it inherently safe.

Threats include malicious links, embedded HTML, unexpected frontmatter, oversized files, parser exploits, prompt injection, hidden Unicode, and malicious paths.

### Controls

- parser limits;
- safe Markdown rendering;
- unsafe raw HTML disabled by default in web surfaces;
- path normalization;
- size limits;
- schema validation;
- body text treated as untrusted data when passed to models.

---

## 23. P1: Git history as a confidentiality trap

Deleting a file from the working tree does not erase it from Git history.

### Risks

- secrets remain recoverable;
- sensitive information survives scope changes;
- cloned repositories cannot be remotely revoked.

### Controls

- repository/bundle boundaries may need to align with access boundaries;
- do not rely solely on frontmatter ACLs;
- scan secrets before commit;
- document history-rewrite recovery for accidental sensitive commits;
- consider cloned historical content part of the user's possession.

---

## 24. P0/P1: Provider namespace misconfiguration

### Scenario

Two tenants, teams, or projects are accidentally mapped to the same Hindsight bank or provider namespace.

### Controls

- deterministic mapping owned by Chronicle;
- uniqueness constraints;
- provider namespace registry;
- no caller-supplied raw bank IDs;
- startup validation;
- isolation and migration tests.

---

## 25. P1: Memory-provider compromise

### Controls

- no direct untrusted-client exposure;
- network isolation;
- least-privilege database access;
- adapter validation;
- pinned provider versions;
- SBOM/dependency monitoring;
- Chronicle performs authorization independently;
- institutional knowledge remains usable if memory provider is disabled.

---

## 26. P1: Model output used as executable input

Model output may contain shell commands, SQL, HTML, URLs, code, or tool arguments.

### Controls

- model output is never trusted executable input;
- validate structured outputs;
- parameterize database operations;
- restrict shell/tool execution;
- separate proposal from execution;
- authorize each tool call independently.

---

## 27. P0/P1: Excessive agency

An agent may be capable of reading memory, writing memory, modifying Git, calling tools, and interacting with external systems. That combination can amplify prompt injection or agent compromise.

### Controls

- minimum capabilities;
- separate read/write permissions;
- confirmation/policy gates for high-impact operations;
- short-lived delegated credentials;
- per-agent tool allowlists;
- per-project scope;
- rate limiting;
- audit.

---

## 28. P2: Unbounded consumption

Possible causes include repeated reflection jobs, recursive agents, unbounded memory writes, large embedding jobs, oversized documents, or repeated context expansion.

### Controls

- quotas;
- memory size limits;
- request-body limits;
- context budgets;
- worker concurrency limits;
- model budgets;
- job retry ceilings;
- backpressure;
- circuit breakers;
- per-principal rate limits.

---

## 29. P2: Retrieval denial of service

Attackers may flood queries, create huge memories, cause expensive reranking, overwhelm Hindsight, or exhaust database connections.

### Controls

- rate limits;
- query budgets;
- bounded top-k;
- pagination;
- timeouts;
- provider circuit breakers;
- connection-pool limits;
- worker isolation from interactive requests.

---

## 30. P1: Cache leakage

### Scenario

A context package created for one security context is reused for another.

### Required cache key inputs

At minimum:

```text
tenant/security domain
effective principal
agent/application identity where relevant
scope set
policy version
classification constraints
query/context key
```

Sensitive context should use a short cache lifetime or no shared cache.

---

## 31. P1: Derived-index leakage

A full-text/vector index can expose content the canonical source would deny.

### Controls

- index security metadata;
- query authorized partitions;
- per-result authorization as defense in depth;
- purge derived entries after boundary changes;
- derived indexes are rebuildable;
- automated leakage tests.

---

## 32. P2: Entity-resolution collision

Two different people, projects, systems, or customers may be merged into one entity. This creates both correctness and confidentiality problems.

### Controls

- stable source identifiers;
- confidence thresholds;
- reversible merges;
- scope-aware matching;
- human review for sensitive merges;
- no automatic cross-tenant entity merge.

---

## 33. P1: Malicious correction or forgetting

A principal may try to erase legitimate organizational history or replace correct memory with a false correction.

### Controls

- resource/scope authorization;
- correction creates a traceable transition;
- institutional knowledge governed separately;
- retention/legal-hold policy may override ordinary deletion;
- high-authority deletion may require approval;
- audit.

---

## 34. P1/P2: Audit log leakage and tampering

Audit logs may leak resource names, identities, queries, or snippets.

### Controls

- log metadata rather than full content;
- redact secrets;
- restrict audit access;
- define retention;
- protect transport;
- application roles cannot update/delete audit events;
- use dedicated database permissions;
- consider append-only external sinks for higher-assurance deployments.

---

## 35. P1: Compromised administrator

Administrator compromise can bypass many application controls.

### Controls

- least-privilege admin roles;
- MFA through upstream IdP;
- separation of duties where required;
- privileged-action audit;
- no shared admin accounts;
- emergency recovery process;
- avoid placing every secret in one admin interface.

---

## 36. P1: Docker misconfiguration

Risks include public database ports, direct Hindsight exposure, privileged containers, Docker socket mounts, root execution, or committed `.env` secrets.

### Default Compose controls

- expose only required public ports;
- use internal networks;
- do not mount Docker socket;
- avoid privileged mode;
- drop unnecessary capabilities;
- use read-only mounts where practical;
- run Chronicle as non-root where feasible;
- ship `.env.example`, never real secrets;
- document production TLS/reverse proxy requirements.

---

## 37. P1: Container image compromise

### Controls

- pin images;
- generate SBOMs;
- scan vulnerabilities;
- publish provenance/attestations;
- use minimal final images;
- avoid `latest` in released Compose files;
- automate dependency-update proposals with review.

---

## 38. P1: Open-source supply-chain compromise

Possible vectors:

- malicious dependency;
- maintainer-account compromise;
- compromised CI action;
- typosquatted package;
- malicious PR;
- release-token compromise.

### Controls

- branch protection;
- required review;
- pinned CI actions;
- least-privilege CI tokens;
- dependency review;
- secret scanning;
- artifact attestations;
- SBOMs;
- DCO/contributor traceability;
- release-role separation;
- OpenSSF Scorecard monitoring.

---

## 39. P1: Source ACL drift

### Scenario

A source item used to be visible to a user and is later restricted, but Chronicle still exposes an indexed copy.

### Controls

- source ACL synchronization;
- ingestion records the source authorization context;
- revocation triggers re-evaluation;
- source-derived content is not automatically independently shareable;
- connector policy defines whether source content may become institutional knowledge.

---

## 40. P0/P1: Inference disclosure

Even when raw data is hidden, Chronicle might reveal protected information through a summary or inference.

Example: a caller cannot access HR records, but Chronicle states a sensitive employment fact derived from them.

### Controls

- derived content inherits source restrictions;
- summaries inherit the most restrictive relevant classification;
- context assembler tracks source sensitivity;
- high-sensitivity inference cannot automatically downgrade itself.

---

## 41. P1: Provenance laundering

An attacker may combine many low-authority sources to make a false claim appear trustworthy.

### Controls

- source count is not authority;
- independence of sources is considered;
- repeated copies of one origin are deduplicated;
- authority survives consolidation;
- model-generated agreement is not independent verification.

---

## 42. P1: Cross-agent contamination

One agent's experimental or incorrect memory may influence another agent outside the intended scope.

### Controls

- explicit agent/project scope;
- promotion rules;
- experimental memory remains isolated;
- shared memory requires permission;
- shared observations may require verification.

---

## 43. P1: Personal memory leaking into organization memory

### Controls

- personal/user scope is distinct from team/org;
- promotion is explicit;
- UI clearly identifies target scope;
- agents cannot widen scope during retention;
- automated user-to-org leakage tests.

---

## 44. P1: Compromised external MCP server

External MCP servers may return hostile content or tools.

### Controls

- external MCP content is untrusted by default;
- allowlist servers/tools;
- use separate credentials;
- no token passthrough;
- validate outputs;
- assign explicit connector authority;
- enforce network egress policy.

---

## 45. P1: Tool-description injection

Tool metadata itself can contain misleading instructions.

### Controls

- only approved MCP servers can register tools;
- tool metadata is not promoted into trusted policy;
- tool selection remains constrained by allowlist and capability policy.

---

## 46. P1: Connector privilege escalation

A connector may use a service account with more access than the requesting user.

### Preferred order

1. user-delegated credentials with source authorization;
2. service account plus explicit Chronicle-side ACL mapping;
3. broad service credentials only with strong policy controls and documented risk.

Connector credentials never imply caller authorization automatically.

---

## 47. P1: Incomplete deletion propagation

### Scenario

Chronicle deletes a record, but the same content remains in Hindsight, embeddings, caches, graph projections, backups, or Git history.

### Controls

- deletion workflow enumerates derived locations;
- provider deletion contract;
- cache invalidation;
- index purge;
- documented backup retention;
- Git-specific erasure policy;
- deletion completion status.

---

## 48. P1: Hosted model provider logging

A hosted model provider may retain prompts or telemetry.

### Controls

- document provider policy;
- classification-aware routing;
- first-class local model option;
- minimize sent context;
- use enterprise/provider controls where applicable;
- never assume remote inference is ephemeral.

---

## 49. P1: Unsafe reflection and consolidation

Reflection may create stronger claims than the evidence supports.

### Controls

- derived epistemic status retained;
- observations link evidence;
- confidence/authority do not automatically increase;
- high-impact knowledge requires review;
- benchmark overgeneralization and hallucination.

---

## 50. P2: Runaway knowledge proposals

An agent may generate large numbers of low-value proposals and overwhelm reviewers.

### Controls

- deduplication;
- minimum support threshold;
- proposal budget;
- batching;
- ranking;
- per-agent limits;
- review queue metrics;
- no PR for every observation.

---

## 51. P1/P2: Stale approved knowledge

Human approval does not make content permanently correct.

### Controls

- `stale_after` metadata;
- owners;
- scheduled revalidation;
- source freshness checks;
- supersession;
- visible stale state.

---

## 52. P1: Unauthorized knowledge approval

### Controls

- `knowledge.approve` separate from `knowledge.propose`;
- reviewer policy by knowledge class;
- Git review identity mapped to Chronicle identity;
- optional no-self-approval rules;
- approval audit.

---

## 53. P0/P1: Organization-wide write as a default

Chronicle must not use organization-wide memory as a convenient default.

### Controls

- narrowest reasonable default scope;
- explicit shared scope required;
- personal/project scope preferred;
- organization scope treated as privileged.

---

## 54. P1: Unsafe memory import

Bulk import from another system may introduce stale records, incorrect scopes, missing provenance, secrets, or incompatible authority labels.

### Controls

- import staging;
- low authority by default;
- provenance preservation;
- secret scan;
- mapping review;
- dry-run report;
- quarantine invalid records.

---

## 55. P1: Backup exposure

Backups may contain the entire organization's memory and knowledge state.

### Controls

- encrypted backup storage;
- strict access controls;
- documented retention;
- restore testing;
- no public backup buckets;
- secrets handled separately where practical.

---

## 56. P1/P2: Telemetry exposure

Metrics and traces can accidentally include prompts, IDs, or query text.

### Controls

- no raw memory content in metrics;
- trace attributes are allowlisted;
- sensitive fields redacted;
- query logging configurable;
- telemetry access restricted.

---

## 57. P1: Development defaults reaching production

Examples include mock identity, default passwords, open admin endpoints, debug logs, or directly exposed provider ports.

### Controls

- explicit development mode;
- startup rejects unsafe production combinations;
- no universal default credentials;
- `chronicle doctor` validates common security mistakes.

---

## 58. Risk rating

Chronicle should rate threats using:

```text
Impact: Low / Medium / High / Critical
Likelihood: Low / Medium / High
```

Security boundary violations should generally rank above retrieval-quality issues even when they are less frequent.

---

## 59. Initial risk register

| Threat | Impact | Likelihood | Priority |
|---|---|---:|---:|
| Cross-scope disclosure | Critical | Medium | P0 |
| Unauthorized shared-memory write | Critical | Medium | P0 |
| Memory poisoning | High | High | P0 |
| Indirect prompt injection | High | High | P0 |
| Confused-deputy agent access | Critical | Medium | P0 |
| Knowledge-promotion abuse | High | Medium | P0 |
| Provenance forgery | High | Medium | P0 |
| Secret ingestion | High | High | P0 |
| Source ACL drift | High | Medium | P1 |
| Derived-index leakage | Critical | Low-Medium | P1 |
| MCP token/audience error | High | Medium | P1 |
| Hosted-model disclosure | High | Medium | P1 |
| Supply-chain compromise | Critical | Low-Medium | P1 |
| Git-history leakage | High | Medium | P1 |
| Stale memory as live truth | High | High | P1 |
| Entity collision | Medium-High | Medium | P2 |
| Unbounded consumption | Medium | High | P2 |
| Provider outage | Medium | Medium | P2 |
| Reviewer overload | Medium | Medium | P2 |

---

## 60. Security requirements for the MVP

The proof of concept must not skip basic security because it is early.

### Identity

- every request has an actor;
- agent and human identities can be distinguished;
- anonymous access is disabled except for deliberately public endpoints.

### Authorization

- explicit read/write checks;
- project/user isolation;
- no caller-supplied raw Hindsight bank authority;
- shared-memory writes are restricted.

### Content safety

- secret screening before memory write;
- source trust labels;
- retrieved content treated as data.

### Knowledge governance

- candidate and approved states are distinct;
- generated proposals retain provenance;
- stable high-authority knowledge requires authorized review.

### Audit

At minimum:

- memory writes;
- knowledge proposals/approvals;
- policy changes;
- deletion/correction.

### Deployment

- Hindsight is not publicly exposed by default;
- PostgreSQL is not publicly exposed by default;
- dependency images are pinned;
- no default real credentials.

---

## 61. Required security tests

Chronicle should maintain automated tests for at least:

```text
user A cannot recall user B memory
project A cannot recall project B memory
agent cannot exceed delegated project scope
agent cannot select arbitrary provider bank
agent cannot write organization scope without permission
memory write containing a test secret is blocked or safely handled
untrusted source instruction does not become trusted instruction
deleted memory disappears from normal retrieval
superseded memory is not returned as current
stale source is not presented as live truth
knowledge proposal retains evidence
unapproved proposal is not retrieved as stable knowledge
approved knowledge requires an authorized reviewer
derived index does not bypass source scope
cache result is not reused across security contexts
provider outage does not cause fabricated context
MCP token for another resource is rejected
audit entry identifies acting agent and delegated human
```

Security-isolation tests should be release-blocking.

---

## 62. Adversarial benchmark scenarios

The future benchmark suite should contain attacks, not only quality measurements.

### Prompt-injection persistence

Inject hostile instructions into a source and verify they do not become durable trusted instruction.

### Poisoned repeated evidence

Submit the same false claim through many copied sources and verify duplicate count does not manufacture authority.

### Scope collision

Use semantically similar documents in different projects and verify retrieval does not cross the boundary.

### Supersession attack

Attempt to supersede high-authority knowledge using low-authority agent memory.

### Delegation attack

Give the human broad access but the agent narrow access and verify the agent remains narrow.

### Secret persistence

Expose a synthetic credential and verify it is not retained in memory, knowledge, or logs.

### Approval bypass

Attempt to retrieve candidate knowledge as approved knowledge.

---

## 63. Secure Docker baseline

The default Chronicle image should aim for:

- non-root runtime where feasible;
- minimal base image;
- no unnecessary build tools in the final stage;
- read-only root filesystem where practical;
- writable volumes only where required;
- no Docker socket;
- no privileged mode;
- no unnecessary capabilities;
- explicit health checks.

Compose should:

- use internal networks;
- expose only required ports;
- pin service versions;
- keep databases internal;
- avoid embedding secrets.

---

## 64. Secure GitHub/open-source baseline

The repository should eventually enable:

- branch protection/rulesets;
- required PR review;
- required CI;
- dependency review;
- Dependabot;
- secret scanning;
- code scanning;
- DCO;
- private vulnerability reporting;
- release attestations;
- SBOM generation;
- OpenSSF Scorecard.

Security reports must not be filed as public issues when disclosure would create risk.

---

## 65. Vulnerability disclosure

Chronicle should publish `SECURITY.md` before broad adoption.

It should state:

- supported versions;
- private reporting method;
- expected acknowledgement;
- coordinated disclosure process;
- security-release process;
- CVE/advisory approach where applicable.

---

## 66. Security ownership

At project launch, Arios Technologies acts as security steward.

The governance model should later define:

- who can receive private reports;
- who can approve security releases;
- who can modify security policy;
- how security maintainers are appointed;
- how conflicts are handled.

---

## 67. Privacy considerations

Chronicle may store information about employees, customers, or other individuals.

The architecture should support:

- data minimization;
- purpose limitation;
- configurable retention;
- access control;
- correction;
- deletion where legally and technically applicable;
- export;
- classification.

Chronicle should not claim regulatory compliance merely because these controls exist. Deployment-specific compliance depends on configuration, data, jurisdiction, and operating process.

---

## 68. Classification propagation

Derived content should inherit the most restrictive relevant classification unless a documented policy safely permits downgrade.

Example:

```text
restricted source
   -> summary
   -> observation
   -> knowledge proposal
```

The summary does not become `internal` merely because it contains fewer words.

---

## 69. Human factors

Security controls reviewers cannot understand will be bypassed.

Review surfaces should make important facts visible:

- generated vs human-authored;
- source provenance;
- authority;
- scope;
- classification;
- stale status;
- superseded status;
- acting agent;
- supporting evidence.

Chronicle should not bury those facts behind an advanced panel.

---

## 70. Threat-model maintenance

This document should be revisited when Chronicle adds:

- a new memory provider;
- federation;
- cross-organization memory sharing;
- write-capable systems-of-record connectors;
- new MCP transports;
- automatic knowledge approval;
- new identity models;
- managed hosting;
- mobile clients;
- browser extensions;
- custom graph storage.

Major architecture RFCs should include a threat-model impact section.

---

## 71. Security gates by maturity

### Before first public code release

- threat model exists;
- security policy exists;
- dependency scanning;
- secret scanning;
- no default credentials.

### Before usable alpha

- principal model;
- basic authorization;
- scoped Hindsight access;
- audit;
- secret screening;
- Git/OKF review state.

### Before beta

- adversarial isolation suite;
- MCP auth hardening;
- retention/deletion tests;
- provider failure tests;
- supply-chain controls;
- SBOM.

### Before 1.0

- production authorization model;
- tested backup/restore;
- security review;
- threat model updated from implementation;
- supported-version policy;
- vulnerability reporting/release process;
- documented hardening guide.

---

## 72. Standards and guidance used

Chronicle should track current upstream guidance rather than inventing an isolated AI-security vocabulary.

Primary inputs for this threat model include:

- OWASP Agentic AI — Threats and Mitigations;
- OWASP GenAI / LLM Top 10;
- Model Context Protocol authorization/security guidance;
- NIST AI Risk Management Framework and Generative AI Profile;
- OpenSSF secure-development and threat-modeling practices.

These are reference inputs, not claims of certification.

---

## 73. References

- OWASP Agentic AI — Threats and Mitigations
  https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/

- OWASP GenAI / LLM Top 10
  https://genai.owasp.org/llm-top-10/

- OWASP Prompt Injection guidance
  https://genai.owasp.org/llmrisk/llm01-prompt-injection/

- Model Context Protocol — 2026-07-28 specification release notes
  https://blog.modelcontextprotocol.io/posts/2026-07-28/

- NIST AI Risk Management Framework
  https://www.nist.gov/itl/ai-risk-management-framework

- NIST AI 600-1 — Generative AI Profile
  https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

- OpenSSF — secure software development resources
  https://best.openssf.org/developers.html

- OpenSSF threat-modeling training material
  https://lfd121.openssf.org/lfd121

---

## 74. Decisions that must follow from this model

Several upcoming architecture choices should not be made independently of the threat model.

### Authorization engine

It must support Chronicle's principal + agent + resource relationship model.

### Hindsight bank mapping

It must prove hard isolation wherever Chronicle needs a hard security boundary.

### Git bundle strategy

It must account for the fact that Git history cannot enforce per-file access after clone.

### MCP authentication

It must preserve agent/workload identity and resource-scoped authorization.

### Model routing

It must account for information classification and egress policy.

### Derived search

It must not create a bypass around canonical access control.

---

## 75. Closing security rule

Chronicle's security model should assume that:

- people make mistakes;
- agents can be manipulated;
- models can be wrong;
- retrieved content can be hostile;
- external systems can be compromised;
- memory can outlive the session that created it.

The platform must therefore place trust in explicit identity, enforceable policy, provenance, review, and clear security boundaries rather than in a model's willingness to follow instructions.

That matters more for Chronicle than for many ordinary applications because Chronicle's job is to remember.
