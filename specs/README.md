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
| [`kodhama-spec-0001-family-plugin-release-and-distribution-metadata`](0001-family-plugin-release-and-distribution-metadata.md) | 2 | superseded | Historical family release-certification contract; retired by `kodhama-0017` |
| [`kodhama-spec-0002-bounded-pre-agent-provisioner`](0002-bounded-pre-agent-provisioner.md) | 3 | superseded | Historical universal provisioner contract; retired by `kodhama-0017` |
| [`kodhama-spec-0003-marketplace-test-observation`](0003-marketplace-test-observation.md) | 1 | superseded | Historical observation record; retired by `kodhama-0025` |
| [`kodhama-spec-0004-ci-marketplace-setup-skill`](0004-ci-marketplace-setup-skill.md) | 5 | approved | Host-independent authoring of caller-selected Claude/Codex marketplace setup in GitHub Actions |
| [`kodhama-spec-0005-issue-taxonomy-skill-publication`](0005-issue-taxonomy-skill-publication.md) | 12 | approved | Publishing the issue-convention skill and its provisioning actuator into the Kodhama plugin |

Specs 0001, 0002 and 0003 are historical records, not implementation inputs.
Spec 0004 implements the CI marketplace-setup skill retained by
`kodhama-0017-retire-family-release-certification`. Its other retained goal —
recording which marketplace a test exercised — is met by the GitHub Actions run
log rather than a schema, per `kodhama-0025`.
Spec 0005 implements the delivery half of `kodhama-0026-issue-taxonomy`: it
covers publication only, and asserts no scope for the plugin that carries the
skill. **It also changes what this repository distributes in both
directions**, which the two retained goals above do not anticipate:
`kodhama-0017` line 33 says Stewards *"retains only a narrow future
distribution goal"* and its **AC3** says current repository scope *"describes
only"* those two items — the section `kodhama-0025` amended is **§2**. Spec
0005 adds a third and fourth distributed thing, and drops the
marketplace-metadata description, since per `kodhama-0025` that goal is now met
by the run log rather than by anything the door distributes. Those criteria are
frozen records rather than statements of present state, so spec 0005 does not
edit them; the **disclosure** debt is parked as its open question 6.

## Validation disclosure

[Issue #20](https://github.com/kodhama/stewards/issues/20) records malformed
legacy decision metadata that blocks a literal full-corpus validation PASS.
It does not block change-scoped validation of new artifacts whose own strict
YAML and references are valid. New specs must not copy the legacy metadata
forms, and no spec self-check may claim that issue is resolved.
