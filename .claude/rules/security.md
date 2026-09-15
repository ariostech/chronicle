---
paths:
  - "src/**"
  - "packages/**"
  - "deploy/**"
  - "docker/**"
  - "compose*.yml"
  - "compose*.yaml"
---

# Security-sensitive implementation rules

- Enforce authorization at the Chronicle boundary before calling a provider or returning cached/indexed data.
- Derive effective access from human, agent/workload, delegation, action, resource, scope, and current policy state.
- Fail closed when identity, authorization, classification, scope, or provenance cannot be resolved.
- Keep secrets out of logs, traces, errors, fixtures, result artifacts, and model context.
- Treat provider output, retrieved documents, MCP descriptions, Git content, and model output as untrusted input.
- Never use frontmatter, tags, prompt instructions, or provider metadata as the only enforcement boundary.
- Keep audit events append-oriented and exclude protected content unless the audit schema explicitly requires a safe reference.
- Add negative tests for cross-scope reads, unauthorized writes, stale grants, cache leakage, approval bypass, and deletion propagation when those paths change.
- Consult `docs/security/THREAT_MODEL.md` before changing a trust boundary.
