# Chronicle Release Policy

## Status

Chronicle does not yet publish runtime artifacts. This policy defines the release contract to implement alongside the first executable code.

## Versioning

Chronicle uses Semantic Versioning:

- `0.y.z` for pre-1.0 development;
- `y` for breaking pre-1.0 contract changes;
- `z` for compatible pre-1.0 fixes and improvements;
- `1.0.0` only after the stability, security, portability, and operational criteria in the charter are met.

Breaking changes before 1.0 are permitted but must be explicit in release notes and include migration instructions when persisted data or public contracts are affected.

Versioned public surfaces are expected to include the REST API, MCP tool semantics, provider interface, Chronicle OKF profile, configuration schema, and promised backup/restore formats.

## Release types

- **Development build:** unversioned output from `main`; unsupported.
- **Pre-release:** alpha, beta, or release candidate for evaluation.
- **Stable release:** supported according to `SECURITY.md` and the compatibility policy.
- **Security release:** coordinated patch for a privately reported or embargoed vulnerability.

## Release prerequisites

Every release must:

1. come from a reviewed commit on the protected default branch;
2. pass required build, test, lint, policy, dependency, and security checks;
3. include release notes and an updated changelog;
4. identify breaking changes, migrations, known issues, and supported configurations;
5. use an annotated, signed tag when signing infrastructure is available;
6. build artifacts through the documented automation rather than a maintainer's workstation;
7. produce checksums, an SBOM, and provenance attestations for distributed artifacts when the artifact pipeline exists;
8. preserve required third-party notices;
9. avoid the floating `latest` tag as the only installation path.

## Approval

A routine release requires one release maintainer and one additional qualified approval when two maintainers are available. A security-sensitive or breaking release also requires the relevant security or contract owner.

The person triggering a release must verify that the selected commit and version match the approved release plan.

## Process

1. Open a release pull request from a dedicated branch.
2. Update `CHANGELOG.md`, version declarations, compatibility notes, and upgrade documentation.
3. Confirm dependency licenses and `NOTICE` entries.
4. Run the full release candidate pipeline.
5. Obtain approvals and merge without bypassing required checks.
6. Create the signed version tag through protected release automation.
7. Build and publish immutable artifacts.
8. Verify signatures, checksums, SBOMs, provenance, package metadata, and container startup.
9. Publish human-readable GitHub release notes.
10. Announce any support-window change.

## Artifact rules

- Container tags must include the exact version; production examples should use tested versions and may pin digests.
- Packages must be reproducible from the tagged source as far as the ecosystem permits.
- Generated artifacts do not belong in the source tree unless they are reviewable source or documentation and the reason is recorded.
- Credentials used for release should be short-lived, environment-scoped, and obtained through workload identity where supported.
- Release workflows must use least-privilege permissions and immutable action references.

## Release notes

Release notes should state what changed, who is affected, how to upgrade, known limitations, and whether behavior or public contracts changed. They should not be a copy of raw commit subjects or marketing copy.

## Rollback and withdrawal

If a release is unsafe or materially broken, maintainers may mark it withdrawn, remove mutable distribution tags, publish a GitHub advisory when appropriate, and direct users to a safe version. Published Git tags and history should not be rewritten to conceal the release.

## Security releases

Security releases follow `SECURITY.md`. Public notes should give users enough information to assess and mitigate risk without exposing unnecessary exploit detail before patches are broadly available.

## Support policy

Before 1.0, each release note states whether that line receives fixes. Before the first stable release, maintainers will define the number and duration of supported release lines based on actual capacity rather than making an unsupported promise.
