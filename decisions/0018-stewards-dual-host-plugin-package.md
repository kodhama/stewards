---
id: kodhama-0018-stewards-dual-host-plugin-package
type: decision
status: approved  # maintainer approved the plan on 2026-07-24; independent adversary returned SOUND
depends_on: [kodhama-0017-retire-family-release-certification]
owner: agent
updated: 2026-07-24
provenance: "maintainer intent, 2026-07-24: replicate Grove's small SemVer, VERSION, surface-metadata, and dual-plugin-declaration approach while keeping every product's version and release independent"
---

# Decision: package the Stewards skill as an independent dual-host plugin

## Decision state

**Decided** (maintainer, 2026-07-24):

- Stewards will ship its marketplace-setup skill in a Stewards-owned plugin
  named `stewards`.
- The Stewards plugin independently adopts Grove's small package shape:
  - one SemVer `VERSION` file as the plugin's version authority;
  - one Claude plugin manifest and one Codex plugin manifest carrying that
    same version;
  - one product-owned `surfaces.json` carrying that same version; and
  - one lightweight parity check across those four carriers.
- After each host package satisfies that catalog's standing admission
  boundary, the Claude and Codex Stewards marketplaces will both point to the
  same Stewards-owned plugin source.
- This is a product-local choice for the Stewards plugin, not a family version,
  shared bump policy, synchronized release, or Stewards-owned requirement for
  another product.
- Trellis, Grove, Wisp, and later consumers decide independently whether to
  adopt the same approach and independently own their version, bump, release,
  surface claims, and evidence.

**Open** (0):

- None.

**Parked** (0):

- None. Consumer adoption is owned by consumer decisions during rollout, not
  deferred Stewards design.

## Context

Approved decision `kodhama-0017` authorizes one Stewards-owned generic
CI marketplace-setup skill while explicitly retiring family-wide SemVer,
carrier-parity, release, and support machinery. It also preserves each
product's freedom to choose those mechanisms locally.

Grove demonstrates a useful small local pattern: its plugin has one SemVer
`VERSION`, host-specific Claude and Codex plugin manifests with the same
version, and version-bound product surface metadata. Grove also has extensive
release validation, qualification, tagging, and evidence machinery. Only the
small package shape is needed to distribute the Stewards skill; the rest is
Grove-specific and is not adopted here.

The maintainer clarified that the commonality is the approach, never the
version value: different products must retain different versions and may bump
or release at different times.

## Decision

### 1. Stewards owns one independently versioned plugin

The plugin source is rooted at `plugins/stewards/` and contains:

| Path | Authority |
|---|---|
| `VERSION` | The Stewards plugin's one SemVer version authority. |
| `.claude-plugin/plugin.json` | Claude host declaration; its `name` is `stewards` and its `version` equals `VERSION`. |
| `.codex-plugin/plugin.json` | Codex host declaration; its `name` is `stewards` and its `version` equals `VERSION`. |
| `surfaces.json` | Stewards-owned surface metadata; its top-level `version` equals `VERSION`. |
| `skills/setup-ci-marketplace/SKILL.md` | The shared authoring skill consumed by both host declarations. |

The two host manifests may carry host-specific descriptions and interface
metadata. They declare the same plugin identity and package version but do not
need byte-identical host metadata.

### 2. Parity is local and deliberately small

A repository-local check validates:

- `VERSION` is valid SemVer;
- both host manifests parse and declare `name: "stewards"`;
- both host-manifest versions and `surfaces.json.version` exactly equal
  `VERSION`; and
- every admitted Stewards marketplace entry resolves `stewards` to
  `plugins/stewards`; when entries exist in both catalogs, both resolve to
  that same source.

The check does not decide a bump, create or validate a tag, compare another
product's version, derive support, validate product behavior, generate release
history, or approve publication.

### 3. Catalog admission remains a separate evidenced act

Carrier parity makes the package internally coherent; it does not admit the
package to either catalog. Before adding the Stewards plugin to a host catalog,
the change must satisfy that catalog's standing admission boundary. In
particular, `kodhama-0012` requires a valid Codex package and a supported Codex
surface before Codex-catalog admission. Claude admission likewise requires a
valid Claude package and an actually supported Claude surface rather than an
inference from Codex.

The evidence may be a bounded host-native package and skill invocation test.
It stays in this repository with the Stewards product and is reviewed with the
catalog change. The separately ratifiable marketplace-test observation can
later record the marketplace exercised by a run, but it creates no admission
exception and is not itself proof that the skill behaved correctly.

If one host has not met its admission boundary, that catalog entry remains
absent. The other host's evidence, manifest, or catalog presence cannot
substitute for it.

### 4. Surface metadata stays product-owned

`plugins/stewards/surfaces.json` describes only the Stewards plugin's own host
and authoring surfaces. Its schema and rows are implementation input for the
Stewards plugin, not a family surface registry.

The separately ratifiable marketplace-test observation contract may be linked
from a Stewards surface row after a real test. Catalog presence or a surface
row does not establish behavioral support.

### 5. Other products remain independent

This decision creates no required path, version, manifest, surface row, test,
or release for Trellis, Grove, Wisp, or later consumers.

During consumer rollout, each product records its own decision. A product that
adopts the same approach owns its own SemVer value and release cadence.
Stewards neither coordinates those values nor rejects a product for choosing a
different local package mechanism.

## Consequences

- The CI-authoring skill has one product-owned source with native declarations
  for both hosts.
- Stewards dogfoods the small packaging approach before recommending it to
  consumers.
- Host declarations cannot silently drift from the Stewards plugin's own
  version.
- Catalog admission cannot be inferred from carrier parity or the other
  host's evidence.
- Grove's release engine, tag workflow, qualification records, inventories,
  fingerprints, support derivation, and evidence machinery are not copied.
- Consumer packaging decisions and versions remain independent by
  construction.

## Acceptance criteria

- **AC1:** The decision names the five-file Stewards plugin shape and one
  SemVer authority.
- **AC2:** Claude and Codex manifests and `surfaces.json` are required to equal
  the Stewards plugin's `VERSION`.
- **AC3:** Each Stewards marketplace catalog points to the same product-owned
  plugin source only after that host package and supported host surface meet
  the standing catalog-admission boundary with product-owned evidence.
- **AC4:** The parity check is limited to local shape and carrier equality.
- **AC5:** No tag, bump judgment, release engine, qualification system,
  history, approval, support derivation, or cross-product version comparison
  is introduced.
- **AC6:** Every other product retains independent decisions, versions,
  releases, surface metadata, tests, and support claims.

## Open questions

None.

## Self-check (gate)

The decision records the maintainer's settled independent-version intent,
chooses only the minimum package shape needed to distribute the approved
Stewards skill to both hosts, preserves the standing per-host catalog-admission
boundary, and explicitly excludes Grove-specific and retired family machinery.
It is internally complete with no open item and passed the `draft → gated`
self-check before independent soundness review.

## Lifecycle record

The maintainer explicitly approved this independent-version rollout plan and
directed the wave to start on 2026-07-24. After two bounded revisions preserved
the standing host-specific catalog-admission boundary, the independent
decision adversary returned `SOUND`. The `approved` status records that human
intent act; the adversary judgment informs it and does not substitute for it.
