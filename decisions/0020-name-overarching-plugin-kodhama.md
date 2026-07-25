---
id: kodhama-0020-name-overarching-plugin-kodhama
type: decision
status: approved  # maintainer approved 2026-07-25 after the decision adversary returned SOUND
depends_on: [kodhama-0017-retire-family-release-certification, kodhama-0018-stewards-dual-host-plugin-package]
changes: [kodhama-spec-0004-ci-marketplace-setup-skill@v2]
owner: agent
updated: 2026-07-25
provenance: "maintainer intent, 2026-07-25: use Kodhama, with an h, for both the overarching plugin and its managed marketplace path; exact Claude Code 2.1.199 and Codex CLI 0.145.0 also require an explicit local-path marker"
---

# Decision: name the overarching plugin and managed path Kodhama

## Decision state

**Decided** (5):

- The public plugin identity is lowercase `kodhama`; human-facing labels use
  `Kodhama`.
- The package source moves from `plugins/stewards/` to `plugins/kodhama/`.
- The shared skill namespace becomes `kodhama:setup-ci-marketplace`.
- Generated marketplace checkouts use `.kodhama/marketplaces/<m>`, and
  marketplace-add commands identify them as
  `./.kodhama/marketplaces/<m>`.
- Generated registration steps explicitly run from the GitHub workspace root,
  so caller-owned `defaults.run.working-directory` cannot redirect that path.

**Open** (0):

- None.

**Parked** (0):

- None.

## Context

Decision 0018 named the newly packaged plugin `stewards` because it lives in
the Stewards coordination repository. The maintainer has clarified the product
model: Stewards is the parent coordination role for the plugin suite, while
the overarching plugin it now ships should use the suite identity `Kodhama`.
This partially supersedes decision 0018 only where it chose the public plugin
name, package directory, skill namespace, and those paths' derived carriers.

Specification 0004 v1 also requires both host adapters to pass
`.stewards/marketplaces/<m>` to their marketplace-add command.

During issue #14 validation, the exact supported hosts rejected that spelling:

- Claude Code `2.1.199` interpreted it as an invalid GitHub owner/repository
  shorthand; and
- Codex CLI `0.145.0` reported that it was neither an owner/repository, Git
  URL, nor local marketplace path.

Both hosts require an explicit local-path marker such as `./` or an absolute
path.

## Decision

Name the overarching dual-host plugin `kodhama`, display it as `Kodhama`, and
expose its shared skill as `kodhama:setup-ci-marketplace`. Move its package
source to `plugins/kodhama/`; both host manifests and any future catalog
entries use that identity and source.

Generated marketplace checkouts use the product-neutral managed location
`.kodhama/marketplaces/<m>`. Both host adapters pass the exact explicit local
argument `./.kodhama/marketplaces/<m>` to their marketplace-add command.
Each generated registration step sets its working directory to the GitHub
workspace root before resolving that argument.

The explicit `./` is part of the adapter command, not the checkout path. The
repository remains `kodhama/stewards`: repository role and plugin identity are
deliberately different.

An absolute path is rejected because it would make generated YAML depend on a
runner-specific workspace location when both hosts already accept the portable
explicit-relative form.

Origin, revision, listing-root verification, host-state binding, observation
semantics, independent plugin SemVer, and every product-ownership boundary
remain unchanged.

## Consequences

- Specification 0004 advances to v2 and states the executable command form.
- The plugin's `VERSION`, dual host manifests, surface metadata, skill,
  validators, tests, and future catalog pointers move together under the
  `plugins/kodhama/` identity.
- The shipped skill, expected fixtures, and hosted workflow use the
  `.kodhama` managed location and explicit-relative command form.
- The owned registration step's workspace-root binding becomes part of
  convergence comparison and is independent of caller-owned run defaults.
- Existing v1 consumers need to regenerate a matching block before expecting
  marketplace registration to pass on the supported CLIs.
- No plugin installation, host invocation, provisioning service, or new
  marketplace surface is introduced.
- Decision 0018 otherwise stands: the plugin keeps its independent version,
  dual-host package, local carrier parity, per-host admission boundary, and
  product-owned surface metadata.

## Acceptance criteria

- **AC1:** Both host manifests and the package's public identity use lowercase
  `kodhama`, while human-facing labels use `Kodhama`.
- **AC2:** The shared skill is exposed as
  `kodhama:setup-ci-marketplace` from `plugins/kodhama/`.
- **AC3:** Both generated marketplace-add commands use exactly
  `./.kodhama/marketplaces/<m>`.
- **AC4:** The checkout remains `.kodhama/marketplaces/<m>` and retains exact
  origin and revision verification.
- **AC5:** Every generated registration step runs from the GitHub workspace
  root before resolving the explicit-relative marketplace path.
- **AC6:** The change adds no plugin installation or product behavior.
- **AC7:** The exact supported Claude and Codex versions accept the generated
  local source and expose its verified root in their machine-readable listing.
- **AC8:** Decision 0018's independent version, dual-host carriers, parity,
  admission, and product-ownership clauses remain in force.

## Open questions

None.

## Self-check

The decision records the maintainer's explicit Kodhama naming correction and
resolves the observed cross-host adapter failure with the smallest shared
syntax both hosts accept. It partially supersedes only 0018's `stewards`
identity/path choice, preserves the approved packaging and ownership
boundaries, and introduces no new distribution mechanism.

## Lifecycle record

The independent decision adversary returned `SOUND` after the partial-
supersession pointer and workspace-root binding were made explicit. The
maintainer then approved decision 0020 on 2026-07-25. The `approved` status
records that human intent act.
