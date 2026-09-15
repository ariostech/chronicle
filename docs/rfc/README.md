# Requests for Comments

RFCs are Chronicle's public design process for material changes.

An RFC is required for changes to:

- public API, MCP, provider, OKF, or configuration contracts;
- trust boundaries or authorization semantics;
- canonical persistence or migration behavior;
- governance, licensing, or compatibility promises;
- foundational dependencies or architecture with broad project impact.

Small fixes, ordinary implementation details, and choices within an accepted design do not need an RFC.

## Process

1. Copy `TEMPLATE.md` to `NNNN-short-title.md` using the next available number.
2. Open a draft pull request with status `draft`.
3. Identify owners of affected areas and request review.
4. Keep unresolved questions and objections visible.
5. Allow the review period defined in `GOVERNANCE.md`.
6. Set the outcome to `accepted`, `rejected`, or `withdrawn` before merging or closing.

An accepted RFC defines direction. ADRs may still be needed to record concrete implementation decisions.
