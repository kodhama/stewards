# Specs

This directory holds revise-in-place contracts derived from settled Kodhama
decisions. A spec is implementation input only while its `status` is `gated`
or `approved`.

Every spec carries:

- `id`, `type`, `status`, `depends_on`, `implements`, `owner`, and `version`
  frontmatter;
- acceptance scenarios in Given/When/Then form;
- requirements and invariants as EARS `shall` statements;
- `## Open questions`; and
- an honest `## Rubric check`.

Behavioral versions use the counter semantics in `.grove/versioning.md`.
Versioned spec dependencies use `id@vN`; append-only decision dependencies
must not be version-pinned.
`implements` names every approved decision whose obligations the spec
materializes; it is not a substitute for `depends_on`.

## Index

| Spec | Version | Status | Subject |
|---|---:|---|---|
| [`kodhama-spec-0001-family-plugin-release-and-distribution-metadata`](0001-family-plugin-release-and-distribution-metadata.md) | 2 | approved | Family release/surface schemas, surface registry, availability records, validation, generation, and legacy-stock transition |
| [`kodhama-spec-0002-bounded-pre-agent-provisioner`](0002-bounded-pre-agent-provisioner.md) | 3 | approved | Explicit, idempotent Claude/Codex provisioning before local, CI, or cloud/container agent launch |

## Validation disclosure

[Issue #20](https://github.com/kodhama/stewards/issues/20) records malformed
legacy decision metadata that blocks a literal full-corpus validation PASS.
It does not block change-scoped validation of new artifacts whose own strict
YAML and references are valid. New specs must not copy the legacy metadata
forms, and no spec self-check may claim that issue is resolved.
