# Specs

**Every spec here is historical. None is an implementation input** — this
repository builds nothing. It holds decisions, a conductor seat, and a
one-plugin install door.

They are kept, not maintained: `.grove/lifecycle.md` makes `superseded`
terminal and says the original content is never edited away. Read them as
records of what was contracted when, never as present state. The retiring
decision named in each row is the thing to read instead.

## Index

| Spec | Version | Status | Subject |
|---|---:|---|---|
| [`kodhama-spec-0001-family-plugin-release-and-distribution-metadata`](0001-family-plugin-release-and-distribution-metadata.md) | 2 | superseded | Historical family release-certification contract; retired by `kodhama-0017` |
| [`kodhama-spec-0002-bounded-pre-agent-provisioner`](0002-bounded-pre-agent-provisioner.md) | 3 | superseded | Historical universal provisioner contract; retired by `kodhama-0017` |
| [`kodhama-spec-0003-marketplace-test-observation`](0003-marketplace-test-observation.md) | 1 | superseded | Historical observation record; retired by `kodhama-0025` |
| [`kodhama-spec-0004-ci-marketplace-setup-skill`](0004-ci-marketplace-setup-skill.md) | 5 | superseded | Historical CI marketplace-setup skill contract; retired by `kodhama-0030` with the skill |
| [`kodhama-spec-0005-issue-taxonomy-skill-publication`](0005-issue-taxonomy-skill-publication.md) | 13 | superseded | Historical issue-skill publication contract; retired by `kodhama-0030` with the package |

## Validation disclosure

[Issue #20](https://github.com/kodhama/stewards/issues/20) records malformed
legacy decision metadata that blocks a literal full-corpus validation PASS.
It does not block change-scoped validation of new artifacts whose own strict
YAML and references are valid. No spec self-check may claim that issue is
resolved.
