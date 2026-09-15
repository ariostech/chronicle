# Contributing to Chronicle

Chronicle welcomes code, documentation, tests, designs, research, issue triage, and review. The project is pre-alpha, so please coordinate before building a large feature.

## Before you start

1. Read the [Project Charter](docs/project/PROJECT_CHARTER.md), [Technical Specification](docs/spec/TECHNICAL_SPECIFICATION.md), and [Threat Model](docs/security/THREAT_MODEL.md) for the area you plan to change.
2. Search open and closed issues, ADRs, RFCs, and pull requests.
3. Use an issue for a bounded change. Use an RFC for a new public contract, trust-boundary change, major dependency, governance change, or large architectural direction.
4. Never include real credentials, personal records, customer data, proprietary datasets, or confidential incident details in issues, tests, fixtures, or commits.

## Ways to contribute

- clarify a specification or find an inconsistency;
- add adversarial or retrieval-quality test cases;
- improve accessibility or documentation;
- implement an accepted ADR or scoped issue;
- review provider, OKF, MCP, identity, or deployment designs;
- reproduce a bug with synthetic data;
- improve local-first deployment and diagnostics.

## Development status

Language-specific setup commands will be added after the implementation stack is selected. Until then, documentation changes should pass the repository policy checks and keep all relative links valid.

Do not introduce a package manager, framework, database, hosted service, or repository-wide formatter as an incidental part of another change. Propose foundational tooling through an ADR.

## Pull requests

Keep pull requests focused and reviewable. A pull request should include:

- the problem and why it belongs in Chronicle;
- the approach and alternatives considered;
- security, privacy, authorization, provenance, and compatibility impact;
- tests or a clear explanation of why none apply;
- documentation and changelog changes when user-visible behavior changes;
- links to the relevant issue, RFC, or ADR.

Draft pull requests are welcome for early design feedback. A pull request is ready only when its description is complete, automated checks pass, and known follow-up work is stated.

Generated code or prose is not exempt from review. Contributors remain responsible for accuracy, licensing, security, tests, and maintainability regardless of the tools used to create a change.

## Commits and DCO

Every commit must certify the [Developer Certificate of Origin 1.1](https://developercertificate.org/) with a sign-off line:

```text
Signed-off-by: Your Name <your-email@example.com>
```

Create it with:

```bash
git commit -s
```

The sign-off states that you have the right to submit the contribution under the project's license. It is not a copyright assignment.

Prefer clear, imperative commit subjects. Conventional Commit prefixes such as `feat:`, `fix:`, `docs:`, `test:`, `build:`, and `chore:` are encouraged because they make history easier to scan, but exact prefix enforcement is deferred until release automation needs it.

## Review

Reviewers evaluate correctness, scope, tests, security boundaries, compatibility, operational cost, documentation, and consistency with accepted contracts.

Comments marked as required should explain the violated requirement or concrete risk. Suggestions and personal preferences should be identified as such.

Authors should not resolve substantive review threads without agreement from the reviewer who raised them, unless the reviewer is unavailable and another maintainer confirms resolution.

## Tests

All behavior changes need tests at the lowest useful level. Security-boundary changes also need a negative test demonstrating that forbidden access or state transition remains blocked.

Chronicle will treat failures in isolation, authorization, provenance, deletion, and approval-boundary tests as release blockers rather than averaging them into an overall quality score.

Use synthetic identities, organizations, projects, sources, and secrets in test data.

## Documentation

Update the public specification before or with an implementation that changes a public contract. Use:

- ADRs for concrete implementation choices;
- RFCs for material proposals and public contract changes;
- the changelog for user-visible changes;
- the writing guide for repository prose.

## Dependency changes

A new runtime dependency needs a written reason in the pull request. Review its license, maintenance, release integrity, transitive footprint, data access, network behavior, and whether a standard-library or existing dependency can do the job.

Pin GitHub Actions to immutable commit SHAs and retain a version comment. Container images used in released deployment definitions should be pinned to tested versions and, where practical, digests.

## Security reports

Do not open public issues for suspected vulnerabilities or cross-scope data exposure. Follow [SECURITY.md](SECURITY.md).

## Conduct

Participation is subject to the [Code of Conduct](CODE_OF_CONDUCT.md). By contributing, you agree to follow it.

## License

Unless stated otherwise, contributions are licensed under the repository's [Apache License 2.0](LICENSE).
