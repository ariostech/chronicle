# Chronicle Project Charter

**Project:** Chronicle
**Steward:** Arios Technologies
**Project type:** Open-source organizational memory infrastructure
**Status:** Foundational charter
**Charter version:** 0.1
**Date:** 2026-09-11

---

## 1. Purpose of this charter

This charter defines what Chronicle is, why it exists, the principles that should guide it, and the boundaries that should keep it from turning into a general-purpose AI platform.

It is intentionally written before the technical specification and implementation plan. The goal is to give maintainers and contributors a stable reference when individual design choices become difficult.

When a future feature, dependency, or architectural decision conflicts with this charter, the project should either reject the change or amend the charter deliberately. The project should not drift by accident.

---

## 2. Project statement

Chronicle is an open-source organizational memory system for humans and AI agents.

It gives an organization a governed place to retain useful experience, preserve institutional knowledge, connect that knowledge to its sources, and make the right context available to people and agents over time.

Chronicle is designed around a simple distinction:

- **machine memory** captures what agents and systems have experienced, observed, or learned;
- **institutional knowledge** captures what people and the organization can inspect, review, approve, maintain, and understand;
- **systems of record** remain authoritative for live operational facts.

Chronicle connects those layers without pretending they are the same thing.

---

## 3. The problem Chronicle is intended to solve

AI agents are increasingly capable of carrying out useful work, but most organizations still have fragmented context.

Important knowledge is spread across:

- conversations;
- tickets;
- documents;
- source repositories;
- project systems;
- databases;
- internal applications;
- employee memory;
- meeting notes;
- decisions;
- incident history;
- procedures;
- agent sessions.

Today's agent-memory tools are usually good at one part of this problem. Some remember conversations. Some build a knowledge graph. Some provide retrieval over documents. Some maintain agent-specific context. Some help humans work with Markdown.

Those capabilities are useful, but they do not by themselves create organizational memory.

An organization needs to know more than *what can be retrieved*. It also needs to know:

- where the information came from;
- who or what created it;
- whether it is a fact, observation, inference, draft, decision, or approved policy;
- when it was true;
- whether something newer superseded it;
- who may read it;
- who may change it;
- how long it should be retained;
- whether it should become durable organizational knowledge;
- what system remains authoritative for the underlying fact.

Chronicle exists to provide that governed lifecycle.

---

## 4. Vision

Chronicle should become a shared memory and knowledge layer that organizations can use across employees, AI agents, applications, developer tools, and local or hosted models.

A person working in Obsidian, a coding agent operating in a hardened container, an internal assistant, and an automated workflow should all be able to use the same organizational context without receiving the same permissions or the same view of memory.

The long-term goal is not to give every system access to everything the organization knows.

The goal is to make useful context available **safely, selectively, transparently, and with enough provenance that a person can understand why the system believes something**.

---

## 5. Mission

Chronicle will provide an open, self-hostable memory fabric that:

1. captures durable experience without storing indiscriminate conversational noise;
2. preserves provenance and temporal context;
3. separates machine-learned memory from approved institutional knowledge;
4. gives people a readable, editable, version-controlled knowledge layer;
5. enforces organizational scope and access at retrieval and write time;
6. works across models, agents, and applications instead of belonging to one AI vendor;
7. integrates with authoritative systems without replacing them;
8. makes deployment practical for organizations that prefer local and self-hosted infrastructure;
9. supports a healthy open-source ecosystem without withholding governance or security features behind an enterprise paywall.

---

## 6. Core product model

Chronicle should treat organizational context as several related but distinct layers.

### 6.1 Working context

Short-lived context used by a specific agent, application, or session.

Examples:

- the current conversation;
- temporary task state;
- intermediate tool output;
- a coding agent's active work context.

Working context belongs close to the application that needs it. Chronicle may help assemble it, but Chronicle does not need to persist every piece of working context.

### 6.2 Machine memory

Durable context retained because it may be useful later.

Examples:

- a user preference;
- a project event;
- an agent's prior attempt and outcome;
- a recurring failure pattern;
- a relationship between entities;
- an observation consolidated from several experiences.

Machine memory may be represented using structured records, graphs, embeddings, event history, or other machine-oriented forms. It does not need to be exposed to users as one Markdown file per memory.

### 6.3 Institutional knowledge

Human-readable knowledge that the organization intentionally maintains.

Examples:

- decisions and their rationale;
- architecture records;
- procedures;
- runbooks;
- lessons learned;
- policies;
- system documentation;
- project knowledge;
- standards;
- glossaries.

Institutional knowledge should use an open, portable format. Chronicle will use the **Open Knowledge Format (OKF)** as the default standard for this layer and will define a Chronicle profile only where organizational metadata is not covered by the upstream specification.

Git will provide version history and change control. Obsidian will be a first-class human interface, but Chronicle must not require Obsidian for the knowledge to remain usable.

### 6.4 Systems of record

Authoritative operational data remains in the systems responsible for it.

Examples:

- current account balances;
- inventory;
- HR records;
- CRM state;
- deployment state;
- financial transactions;
- production configuration.

Chronicle may retain context about those facts or references to them, but it should query the authoritative source when current truth matters.

---

## 7. Knowledge lifecycle

Chronicle should support a lifecycle in which useful experience can become organizational knowledge without automatically turning agent output into organizational truth.

A typical path is:

```text
source or event
    ↓
experience
    ↓
candidate memory
    ↓
stored memory
    ↓
observation or learned pattern
    ↓
candidate institutional knowledge
    ↓
review
    ↓
approved institutional knowledge
    ↓
future retrieval and action
```

Not every memory should move through the full lifecycle.

A personal preference may remain user-scoped memory indefinitely.

A coding-agent failure may remain project memory.

A pattern observed across repeated incidents may become a proposed lesson.

A proposed lesson may become an approved runbook change only after review.

The system must preserve those distinctions.

---

## 8. Guiding design principles

### 8.1 Memory is selective

Chronicle should not treat complete chat history as a synonym for memory.

Durable memory should earn its place through relevance, utility, policy, or explicit user intent.

### 8.2 Human-readable knowledge is a first-class product surface

Important organizational knowledge must not exist only as vectors, database rows, or graph edges.

People need a readable representation they can inspect, edit, review, discuss, version, and export.

### 8.3 Machine memory and institutional knowledge are different things

Agent observations are not automatically policy.

Summaries are not automatically facts.

Repeated patterns are not automatically organizational truth.

Chronicle must preserve the boundary between what a machine has learned and what the organization has accepted.

### 8.4 Provenance survives transformation

When information moves from source material to extracted fact, observation, summary, or knowledge document, Chronicle should retain enough evidence to explain the chain.

The platform should be able to answer:

> Why does Chronicle believe this?

### 8.5 Time is part of the fact

Chronicle should distinguish:

- when information was observed;
- when it became valid;
- when it stopped being valid;
- when it was superseded;
- when Chronicle learned it.

Historical information should remain queryable where policy permits, while current retrieval should prefer what is valid now.

### 8.6 Retrieval never expands permission

If a user or agent is not permitted to access a source or scope, Chronicle must not reveal that information through memory retrieval, summaries, inferred context, search results, or generated output.

### 8.7 Write access matters as much as read access

A compromised or poorly scoped agent must not be able to write organizational memory outside its authority.

The ability to remember something in a shared scope is a privileged operation.

### 8.8 The platform is model-independent

Chronicle should work with:

- local models;
- hosted models;
- OpenAI-compatible endpoints;
- Ollama;
- llama.cpp;
- model gateways;
- future providers.

No core memory contract should depend on one model vendor.

### 8.9 The platform is agent-independent

Chronicle should work with coding agents, workplace assistants, internal automations, and future agent frameworks through stable protocols such as MCP, REST, and SDKs.

### 8.10 Providers are replaceable

The public Chronicle contract must not be the API contract of its initial memory provider.

Hindsight is the initial memory engine because it already provides useful memory extraction, retrieval, temporal context, observations, reflection, local-model support, and agent integrations.

Chronicle will place Hindsight behind a provider abstraction so that alternative or supplemental engines can be evaluated later.

### 8.11 Open standards are preferred to Chronicle-specific formats

Chronicle should not invent a proprietary representation when a suitable open standard exists.

This includes adopting OKF for institutional knowledge and tracking emerging interoperability standards for shared memory when they are mature enough to use safely.

### 8.12 Canonical data should remain portable

An organization must be able to export its institutional knowledge and move away from Chronicle without losing readable content.

Git + OKF Markdown should remain useful without Chronicle, without Obsidian, and without the original memory engine.

### 8.13 Deployment simplicity is part of the product

A self-hosted open-source project fails if installation requires an architecture consulting engagement.

Chronicle's default deployment must be practical.

The project should maintain a tested Docker Compose stack containing the services required for a useful first installation, including the current memory provider and its dependencies.

### 8.14 Safe defaults are better than clever defaults

When scope, authority, sensitivity, or provenance is ambiguous, Chronicle should prefer not to broaden access or silently promote information.

### 8.15 Complexity must earn its place

Graph databases, vector databases, event stores, queues, policy engines, and specialized infrastructure may all be useful.

They should be added because benchmarks or requirements justify them, not because they make the architecture look sophisticated.

---

## 9. Initial technical direction

The following decisions define the current starting point. They may evolve through the project's RFC and ADR processes, but implementation should assume them until a deliberate decision replaces them.

### Memory engine

**Hindsight** is the initial memory provider.

Chronicle will not expose Hindsight as its public API contract. A provider interface will sit between Chronicle and the memory engine.

### Institutional knowledge

**OKF-compatible Markdown** is the default institutional knowledge representation.

Chronicle-specific organizational fields should be added as a documented OKF profile or extension rather than a fork of the standard.

### Version control

**Git** is the default version-control mechanism for institutional knowledge.

For single-user or local evaluation, Chronicle should be able to initialize and manage a local Git repository without requiring an external Git forge.

Collaborative deployments may connect to GitHub, GitLab, Forgejo, or other Git services.

### Human workspace

**Obsidian** is a first-class human client because it works directly with Markdown, links, metadata, and local files.

Obsidian is not the database and is not required for Chronicle to function.

### Agent interoperability

**MCP** will be a first-class agent integration surface.

REST APIs and SDKs will support applications that should not depend on MCP.

### Models

Local inference is a first-class use case.

Chronicle should support Ollama, llama.cpp, and compatible model gateways alongside approved hosted models.

### Deployment

Docker is the initial deployment target.

The repository will include a maintained Docker Compose configuration that brings up a useful Chronicle installation with the required dependencies.

Hindsight will run as its own service rather than being baked into the Chronicle image.

Chronicle's own API/server, workers, CLI, MCP runtime, migrations, OKF tooling, and bootstrap logic should be packaged into Chronicle-managed images where practical.

### Storage

PostgreSQL is the expected initial transactional store.

Hindsight may use the same PostgreSQL server through a separate database or schema where practical.

Alternative graph/vector substrates, including HelixDB, remain candidates for later provider or storage experiments rather than initial requirements.

---

## 10. Initial service boundaries

The implementation should evolve toward these logical components.

### Chronicle Gateway

The main trusted boundary.

Responsibilities include:

- authentication;
- authorization;
- scope resolution;
- memory-provider routing;
- context assembly;
- provenance;
- retention enforcement;
- policy checks;
- audit;
- source routing;
- knowledge access.

Clients and agents should talk to the Gateway rather than directly to storage engines.

### Memory Provider Layer

A replaceable interface over machine-memory engines.

The first implementation will target Hindsight.

The provider contract should eventually support operations such as:

- retain;
- recall;
- search;
- reflect;
- retrieve evidence;
- retrieve timeline/history;
- correct;
- forget;
- health/capabilities.

### Knowledge Plane

Responsible for:

- OKF parsing and validation;
- Chronicle OKF profile validation;
- Git integration;
- knowledge bundles;
- indexing;
- proposals;
- review/promotion workflow;
- citations;
- freshness;
- knowledge history.

### Context Assembler

Builds a bounded context package from:

- institutional knowledge;
- machine memory;
- current task/session context;
- live systems of record;
- policies and permissions.

The assembler should favor useful context over maximum context.

### MCP Server

Provides a small semantic set of tools rather than mirroring every internal API endpoint.

### Workers

Handle asynchronous work such as:

- memory processing;
- consolidation;
- entity resolution;
- OKF validation;
- indexing;
- stale-content checks;
- knowledge proposal generation;
- retention jobs;
- re-embedding;
- background evaluation.

### Administrative Surface

A later operator-facing UI/API for:

- scopes;
- policies;
- audits;
- memory inspection;
- conflicts;
- retention;
- provider health;
- retrieval diagnostics.

---

## 11. Identity and scope model

Chronicle is intended for organizational use, so identity cannot be an afterthought.

The platform should recognize at least:

- human users;
- agents;
- applications;
- services;
- workloads.

Memory should be scoped explicitly.

Initial scope types should include:

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

The exact hierarchy must be defined by the technical specification rather than hard-coded from this charter.

Chronicle should support narrow, explicit access boundaries and should not assume that all organizational knowledge belongs in one globally readable memory space.

---

## 12. Authority model

Chronicle must represent the difference between evidence and authority.

The technical specification should define the exact model, but the intended ordering is broadly:

1. authoritative system of record;
2. approved institutional knowledge or policy;
3. approved decision;
4. verified memory or observation;
5. direct user or employee statement;
6. agent-derived observation;
7. agent hypothesis or inference.

A lower-authority item should not silently replace a higher-authority source.

---

## 13. Human control

People should be able to inspect and correct the system.

Chronicle should eventually provide practical ways to:

- see what is known about a topic;
- inspect supporting evidence;
- see history and superseded information;
- correct a memory;
- dispute a memory;
- forget or retire a memory where policy permits;
- propose knowledge;
- review proposed knowledge;
- approve institutional knowledge;
- see why an answer used particular context.

Human control is part of the product, not an administrative afterthought.

---

## 14. Security posture

Chronicle should be designed as security-sensitive infrastructure.

It may contain:

- internal project context;
- employee information;
- operational knowledge;
- confidential decisions;
- incident history;
- source-derived context;
- agent-generated observations.

Security decisions therefore belong in the architecture from the beginning.

The project should maintain a threat model before production-oriented implementation proceeds.

The threat model should cover at least:

- cross-user leakage;
- cross-team leakage;
- cross-tenant leakage;
- prompt injection stored as memory;
- memory poisoning;
- malicious or compromised agents;
- privilege escalation;
- unauthorized memory writes;
- unauthorized knowledge promotion;
- source ACL drift;
- data exfiltration;
- stale permissions;
- secret ingestion;
- unsafe connectors;
- vulnerable dependencies;
- compromised model/tool endpoints.

---

## 15. Privacy and retention

Chronicle should not assume that persistent memory is always desirable.

The platform must support:

- data minimization;
- retention policies;
- explicit deletion;
- archival;
- expiration;
- offboarding;
- legal/policy holds where implemented;
- classification;
- scope-specific retention.

Credentials, tokens, secrets, and similar data should be rejected from normal durable memory unless an explicitly designed secure feature requires otherwise.

---

## 16. Open-source principles

Chronicle will be developed as a genuinely useful open-source project under the stewardship of Arios Technologies.

The open-source version should contain the capabilities required to operate Chronicle responsibly.

Core governance and safety features will not be withheld as artificial enterprise gates.

This includes the project's core support for:

- authentication integration;
- authorization;
- multi-user and team use;
- audit;
- self-hosting;
- governance workflows;
- local models;
- MCP;
- OKF/Git knowledge management;
- Obsidian integration;
- backup/export;
- retention;
- core observability hooks.

Arios Technologies may build commercial services around Chronicle, including:

- managed hosting;
- implementation;
- migration;
- enterprise support;
- operational support;
- SLA-backed deployments;
- architecture consulting;
- training;
- managed upgrades;
- custom integration work;
- compliance assistance.

The commercial model should make Chronicle easier to adopt, not make the open-source version deliberately unsafe or incomplete.

---

## 17. Licensing direction

Chronicle will use an OSI-approved open-source license.

The current recommendation is **Apache License 2.0** because of its permissive terms and explicit patent grant.

The final license should be confirmed before the public repository begins accepting substantial third-party contributions.

Contributor policy should favor a low-friction model such as the Developer Certificate of Origin unless future legal or business requirements justify a CLA.

---

## 18. Documentation and project operations

The repository should be treated as part of the product.

Before broad public release, Chronicle should maintain:

- README;
- architecture documentation;
- contribution guide;
- security policy;
- code of conduct;
- governance policy;
- maintainer policy;
- roadmap;
- changelog;
- release policy;
- API/protocol documentation;
- deployment documentation;
- threat model;
- ADRs;
- RFCs for major changes.

The project should follow recognized open-source practices including semantic versioning, human-readable release notes, dependency/security scanning, branch protection, review requirements, reproducible release practices, and supply-chain metadata appropriate to project maturity.

---

## 19. Writing and documentation standard

Chronicle documentation should read like it was written by maintainers who understand the software.

The project should prefer:

- concrete language;
- specific technical claims;
- natural sentence structure;
- explicit trade-offs;
- real examples;
- appropriate uncertainty;
- direct explanations.

Documentation should avoid generic promotional language, repetitive framing, unnecessary headings, formulaic transitions, inflated claims, and the uniform polished tone commonly associated with machine-generated documentation.

Different artifacts should sound appropriate to their purpose. A protocol specification should not sound like a launch post. A security policy should not sound like marketing copy.

A separate writing/style guide should be maintained for human and AI contributors.

---

## 20. Primary users

Chronicle should serve several groups without trying to give them identical interfaces.

### Knowledge workers

People who need organizational context while doing ordinary work.

Primary surface: Obsidian and other future human clients.

### Software developers

People using coding agents and developer tools.

Primary surfaces: MCP, CLI, IDE/coding-agent integrations, project knowledge bundles.

### AI agents and automated workflows

Software that needs persistent context and organizational knowledge.

Primary surfaces: MCP, REST, SDKs.

### Platform operators

People responsible for deployment, identity, security, policy, upgrades, and observability.

Primary surfaces: configuration, APIs, CLI, administrative UI, telemetry.

### Maintainers and knowledge owners

People responsible for approving institutional knowledge and resolving conflicts.

Primary surfaces: Git review workflows, Obsidian, knowledge-management tools.

---

## 21. Project goals

Chronicle should make the following possible.

### Goal A — Shared context without shared exposure

Multiple users and agents can benefit from one organizational memory platform while seeing only the context they are authorized to use.

### Goal B — Durable organizational learning

Useful experiences can survive individual conversations, agents, employees, and tools.

### Goal C — Inspectable memory

Important conclusions can be traced back to their evidence.

### Goal D — Human-readable institutional memory

Organizational knowledge remains readable and maintainable outside the AI system.

### Goal E — Safe knowledge promotion

Machine-learned observations can become institutional knowledge through an explicit review path rather than silent promotion.

### Goal F — Replaceable AI infrastructure

Models, memory engines, and agent frameworks can evolve without forcing the organization to abandon its accumulated knowledge.

### Goal G — Practical self-hosting

An organization can bring up a meaningful deployment without manually assembling a dozen undocumented dependencies.

### Goal H — Open interoperability

Chronicle should prefer standards and stable protocols so that it can participate in the broader agent ecosystem rather than becoming a silo.

---

## 22. Non-goals

Chronicle is not intended to become:

### An LLM provider

Chronicle may route to models, but it does not need to train or host a general-purpose foundation model.

### An agent framework

Chronicle should work with agent frameworks instead of replacing them.

### A replacement for Obsidian

Obsidian is a client over ordinary files. Chronicle should preserve that independence.

### A replacement for Git

Chronicle should use Git's strengths rather than reimplementing version control.

### A replacement for systems of record

ERP, CRM, HRIS, databases, ticketing systems, and similar applications continue to own their authoritative operational state.

### A generic vector database

Chronicle may use vector search, but vector storage is an implementation detail rather than the product.

### A generic graph database

Graph storage may be valuable, but Chronicle should not rebuild an existing database unless a clear requirement justifies it.

### A document-management suite

Chronicle may reference, ingest, or index documents. It does not need to recreate a full enterprise document-management system.

### A universal integration platform

Connectors matter, but the project should first provide good generic interfaces such as MCP, Git, REST, SQL, filesystem, and webhooks before trying to support every SaaS product.

### An autonomous source of organizational truth

Chronicle helps organizations retain and use knowledge. It should not silently elevate model output into policy, fact, or authority.

---

## 23. MVP boundary

The first useful Chronicle release should prove the complete lifecycle rather than maximize feature count.

The MVP should demonstrate:

1. an authenticated user can access Chronicle;
2. the Gateway resolves the user's permitted scopes;
3. Chronicle can retain and retrieve machine memory through Hindsight;
4. Chronicle can read and validate an OKF knowledge bundle stored in Git;
5. an agent can retrieve authorized knowledge and memory through MCP;
6. Obsidian can work with the same human-readable knowledge;
7. agent-derived memory can produce a candidate knowledge change;
8. that change can be reviewed through Git;
9. approved knowledge becomes available to future users and agents;
10. provenance connects the approved knowledge back to its supporting evidence;
11. superseded information remains historically understandable without being treated as current;
12. the full development stack can be started through the supported Docker Compose workflow.

The MVP does not need federation, every enterprise connector, or a custom graph database.

---

## 24. MVP proof scenario

A useful end-to-end acceptance scenario is:

```text
A human creates or edits an OKF knowledge document in Obsidian.
    ↓
The document is committed to Git.
    ↓
Chronicle indexes it.
    ↓
A coding agent starts a fresh session through MCP.
    ↓
Chronicle supplies the relevant authorized project knowledge.
    ↓
The coding agent encounters a repeatable implementation issue.
    ↓
Hindsight retains the experience and supporting evidence.
    ↓
Later evidence supports a durable observation.
    ↓
Chronicle proposes an OKF knowledge update.
    ↓
A human reviews the Git change.
    ↓
The change is merged.
    ↓
The approved knowledge becomes available to future agents and users.
```

If this flow is reliable, understandable, secure, and easy to deploy, Chronicle has proven its central premise.

---

## 25. Success criteria before 1.0

Chronicle should not declare 1.0 merely because it has accumulated features.

Before 1.0, the project should demonstrate:

### Stable contracts

Core APIs, MCP semantics, provider contracts, scope semantics, and knowledge-profile behavior are documented and can be depended on.

### Security

Threat-model findings have been addressed to an appropriate level and automated tests cover the major isolation boundaries.

### Retrieval quality

The benchmark suite shows that Chronicle improves useful context retrieval without unacceptable cross-scope leakage or degradation as memory grows.

### Temporal correctness

Supersession and time-aware queries work consistently.

### Provenance

Important knowledge and memory can be traced to supporting evidence.

### Portability

An organization can export its OKF/Git institutional knowledge and retain usable information without Chronicle.

### Operational maturity

Deployment, upgrades, backups, recovery, logging, metrics, and failure modes are documented.

### Open-source health

Contribution, governance, security reporting, release processes, and maintenance expectations are clear.

---

## 26. Evaluation and benchmarks

Chronicle should maintain an executable benchmark suite rather than relying only on subjective demonstrations.

The suite should eventually measure:

- memory extraction accuracy;
- retrieval precision and recall;
- temporal correctness;
- contradiction handling;
- entity resolution;
- context usefulness;
- cross-scope isolation;
- poisoning resistance;
- stale-memory behavior;
- deletion/retention behavior;
- provenance completeness;
- latency;
- storage growth;
- token overhead;
- behavior after long-running memory accumulation.

Alternative providers and storage engines should earn adoption through these benchmarks.

---

## 27. Deployment expectations

The default developer/self-hosted path should be short enough to document near the top of the README.

The intended experience is approximately:

```bash
git clone <chronicle-repository>
cd chronicle
cp .env.example .env
docker compose up -d
```

The supported stack should take responsibility for bringing up the dependencies it requires.

The initial Compose deployment is expected to include, at minimum:

- Chronicle server/Gateway;
- Chronicle worker runtime where required;
- Chronicle MCP surface;
- Hindsight;
- PostgreSQL with the extensions required by the chosen Hindsight configuration.

Optional Compose profiles may add:

- Ollama/local model infrastructure;
- observability;
- collaborative Git hosting;
- development tooling.

Released stacks should pin compatible dependency versions rather than depending on floating `latest` tags.

---

## 28. Project stewardship and governance

Arios Technologies is the initial project steward.

The project should be open to outside contribution and should document a path from contributor to reviewer and maintainer as the community develops.

The governance model should eventually define:

- maintainer responsibilities;
- decision rights;
- release authority;
- security authority;
- contributor advancement;
- inactivity/removal rules;
- RFC process;
- conflict resolution.

Arios Technologies may retain stewardship while still allowing meaningful technical ownership by trusted community maintainers.

---

## 29. Decision process

Three mechanisms should serve different purposes.

### Charter

Defines the stable project mission and boundaries.

### RFC

Used before significant architectural or public-contract changes.

### ADR

Records a concrete architecture decision once made.

Not every issue needs an RFC. Not every implementation detail needs an ADR.

The project should document practical thresholds so that governance does not become bureaucracy.

---

## 30. Decisions currently considered established

The following are part of the current project direction:

- The project name is **Chronicle**.
- Chronicle is an open-source project stewarded by Arios Technologies.
- Governance and security capabilities belong in the open-source project.
- Hindsight is the initial memory provider.
- The memory provider is hidden behind a Chronicle abstraction.
- Institutional knowledge is human-readable and version-controlled.
- OKF is the default institutional knowledge standard.
- Git is the default version-control mechanism for institutional knowledge.
- Obsidian is a first-class human client but is not a required database.
- MCP is a first-class agent integration protocol.
- Local and self-hosted AI models are first-class deployment options.
- Docker Compose is a first-class installation path.
- Systems of record remain authoritative for live operational state.
- Alternative storage and memory engines will be evaluated through requirements and benchmarks rather than added pre-emptively.

---

## 31. Decisions still to be finalized

The following belong in upcoming specifications or ADRs:

- final OSS license;
- exact scope hierarchy and inheritance rules;
- authorization engine;
- identity-provider integration model;
- Chronicle OKF profile fields;
- Git bundle/repository boundaries;
- knowledge-promotion workflow;
- memory-provider API;
- context-assembly algorithm;
- initial MCP tool contract;
- project implementation language(s);
- monorepo tooling;
- queue/job infrastructure;
- observability stack;
- secret/DLP strategy;
- default local models and embedding models;
- version-support policy;
- backup and recovery design;
- package/container naming;
- public domain and trademark/name clearance.

---

## 32. Immediate next design artifacts

With this charter established, the next foundational artifacts should be:

1. **Chronicle Technical Specification v0.1**
   Define memory, knowledge, evidence, truth, authority, scopes, provenance, time, retention, supersession, and lifecycle semantics.

2. **Chronicle Reference Architecture**
   Turn the charter into concrete services, interfaces, trust boundaries, data flows, and deployment topology.

3. **Chronicle Security and Threat Model**
   Define assets, actors, trust boundaries, threats, abuse cases, and required controls before implementation hardens assumptions.

4. **Open-source repository and governance foundation**
   Establish the repository structure, license, contribution model, issue/PR process, documentation rules, security reporting, CI, release process, and project automation.

5. **Executable benchmark specification**
   Convert the existing memory research into tests that can compare Hindsight and future providers objectively.

6. **Narrow proof of concept**
   Implement the end-to-end human knowledge → agent context → machine memory → proposed knowledge → human review loop described in this charter.

---

## 33. Charter amendment

This charter is expected to evolve, especially before Chronicle reaches 1.0.

Changes that materially alter Chronicle's mission, open-source commitments, product boundaries, authority model, or distinction between machine memory and institutional knowledge should be made explicitly through a reviewed charter amendment.

Implementation convenience alone should not silently redefine the project.

---

## 34. Closing principle

Chronicle should help an organization remember without turning opaque machine state into unquestioned truth.

The platform succeeds when people and agents can benefit from accumulated experience while still being able to answer:

- What do we know?
- Why do we know it?
- Where did it come from?
- When was it true?
- Who is allowed to use it?
- What replaced it?
- Is it memory, inference, approved knowledge, or live operational truth?
- Can it be corrected, retired, or forgotten?

That is the standard the rest of the project should be designed against.
