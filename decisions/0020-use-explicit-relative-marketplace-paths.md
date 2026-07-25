---
id: kodhama-0020-use-explicit-relative-marketplace-paths
type: decision
status: gated
depends_on: [kodhama-0017-retire-family-release-certification]
changes: [kodhama-spec-0004-ci-marketplace-setup-skill@v2]
owner: agent
updated: 2026-07-25
provenance: "hosted-validation preparation for issue #14: exact Claude Code 2.1.199 and Codex CLI 0.145.0 rejected the approved adapter's bare .stewards path as a non-local marketplace source"
---

# Decision: use explicit relative paths for local marketplace registration

## Decision state

**Decided** (1):

- Generated Claude and Codex marketplace-add commands will identify the local
  checkout as `./.stewards/marketplaces/<m>`.

**Open** (0):

- None.

**Parked** (0):

- None.

## Context

Specification 0004 v1 requires both host adapters to pass
`.stewards/marketplaces/<m>` to their marketplace-add command.

During issue #14 validation, the exact supported hosts rejected that spelling:

- Claude Code `2.1.199` interpreted it as an invalid GitHub owner/repository
  shorthand; and
- Codex CLI `0.145.0` reported that it was neither an owner/repository, Git
  URL, nor local marketplace path.

Both hosts require an explicit local-path marker such as `./` or an absolute
path. The generated checkout remains at the same repository-relative location.

## Decision

Use `./.stewards/marketplaces/<m>` as the exact marketplace-add argument for
both version-1 host adapters.

The explicit `./` is part of the adapter command, not the checkout path.
Origin, revision, listing-root verification, host-state binding, observation
semantics, and every ownership boundary remain unchanged.

An absolute path is rejected because it would make generated YAML depend on a
runner-specific workspace location when both hosts already accept the portable
explicit-relative form.

## Consequences

- Specification 0004 advances to v2 and states the executable command form.
- The shipped skill, expected fixtures, and hosted workflow use the same form.
- Existing v1 consumers need to regenerate a matching block before expecting
  marketplace registration to pass on the supported CLIs.
- No plugin installation, host invocation, provisioning service, or new
  marketplace surface is introduced.

## Acceptance criteria

- **AC1:** Both generated marketplace-add commands use exactly
  `./.stewards/marketplaces/<m>`.
- **AC2:** The checkout remains `.stewards/marketplaces/<m>` and retains exact
  origin and revision verification.
- **AC3:** The change adds no plugin installation or product behavior.
- **AC4:** The exact supported Claude and Codex versions accept the generated
  local source and expose its verified root in their machine-readable listing.

## Open questions

None.

## Self-check

The decision resolves one observed cross-host adapter failure with the
smallest shared syntax both hosts accept. It preserves the approved ownership
boundary and introduces no new mechanism or open design choice.
