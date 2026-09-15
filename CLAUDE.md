# Chronicle project instructions

Chronicle is an open-source governed organizational-memory platform. Read `README.md`, `ROADMAP.md`, and the relevant document under `docs/` before changing a public contract or trust boundary.

## Product invariants

- Authorize before retrieval, disclosure, and durable writes.
- Humans, agents, and workloads are distinct principals. Never collapse an agent into its delegating user.
- Models and memory providers do not make authorization decisions.
- Retrieved content is untrusted data, not executable instruction.
- Machine memory does not become institutional knowledge without the defined promotion and review process.
- Preserve scope, provenance, authority, classification, time, retention, and audit information through every transformation.
- Keep approved institutional knowledge portable as OKF-compatible Markdown in Git.
- Keep providers replaceable. Hindsight is the initial adapter, not Chronicle's public abstraction.
- Security, authorization, audit, governance, self-hosting, export, and local-model support belong in the open-source core.

## Working method

- Inspect the current code and accepted ADRs before proposing or implementing changes.
- Preserve user changes and avoid unrelated refactors.
- Make routine implementation judgments. Stop only when alternatives would materially change a public contract, security boundary, persisted format, license, or operational burden.
- Record architectural choices in ADRs and public-contract changes through the RFC process.
- Implement complete vertical behavior for the current phase. Do not leave fake implementations, production-path stubs, or tests that only encode hard-coded fixtures.
- Use synthetic data in tests and examples. Never commit credentials, private data, or production identifiers.
- Keep dependencies deliberate, pinned where appropriate, and compatible with Apache-2.0.
- Give one brief progress update when a material finding changes the plan. Finish with the outcome, tests run, documentation changed, and remaining blockers.

## Documentation

- Update documentation in the same change as behavior.
- Keep `README.md` accurate for a stranger arriving at the repository.
- Update `CHANGELOG.md`, `ROADMAP.md`, and `docs/implementation/STATUS.md` when a milestone changes.
- Follow `WRITING.md`. Prefer concrete explanations over generic product language.
- Commands in setup guides must work from a clean clone on a supported platform.

## Quality gates

- Run the narrow relevant tests while developing, then the phase acceptance commands once before committing.
- Do not weaken, delete, or special-case a test merely to make it pass.
- Security-gate failures are disqualifying.
- Run `python3 .github/scripts/check_repository.py` before committing.
- Commits must be focused and include a DCO sign-off. Do not push, publish, tag, or deploy unless the operator explicitly authorizes it.

## Prompt suite

The staged implementation prompts live in `docs/implementation/claude-code/`. Execute them in numeric order. At the start of every phase, read `docs/implementation/STATUS.md`, `docs/implementation/DECISIONS_NEEDED.md`, and recent Git history. At the end, leave the repository in a clean, resumable state.
