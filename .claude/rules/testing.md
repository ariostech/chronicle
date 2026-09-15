---
paths:
  - "src/**"
  - "packages/**"
  - "tests/**"
  - "test/**"
  - "**/*Test*"
  - "**/*.test.*"
  - "**/*.spec.*"
---

# Testing rules

- Test behavior at public and trust boundaries, not private implementation details.
- Include normal, invalid, unauthorized, stale, conflicting, outage, and deletion cases where relevant.
- Use deterministic clocks, identifiers, seeds, and synthetic fixtures where possible.
- Integration tests must isolate their databases, provider banks, Git repositories, and knowledge bundles.
- Tests must not require production credentials or make unannounced calls to external services.
- A skipped required security test prevents conformance; it is not a pass.
- Preserve failure diagnostics without exposing secrets or protected content.
