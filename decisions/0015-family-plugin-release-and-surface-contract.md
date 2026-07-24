---
id: kodhama-0015-family-plugin-release-and-surface-contract
type: decision
status: superseded  # retired in full by kodhama-0017 (2026-07-24); original approval record remains in this file
depends_on: [kodhama-0002-delivery-channels]
informed_by: [grove/adr-0028-plugin-release-tagging, grove/adr-0031-multi-host-distribution, trellis/decision-0036, kodhama-0013-family-codex-native-product-support]
superseded_by: [kodhama-0017-retire-family-release-certification]
owner: agent
updated: 2026-07-24
provenance: maintainer direction on 2026-07-24 to make one family SemVer and surface-contract strategy, while preserving product-owned implementation and release cadence; artifact approval remains at the human ship gate
---

# Decision: one family plugin release and surface contract, independently applied by every product

> **Superseded by `kodhama-0017-retire-family-release-certification`
> (2026-07-24).** The family SemVer, tag, release-identity, surface-contract,
> and certification architecture is retired. This file remains the historical
> record of the earlier decision.

## Decision state

**Decided** (maintainer direction, 2026-07-24):

- Every plugin distributed through the Kodhama install door uses SemVer as its
  package release identity.
- Stewards owns the common release and surface-contract shape; each product
  owns its version value, bump judgment, release cadence, behavioral support,
  evidence, and product-specific extensions.
- Package version, immutable source identity, and payload/content identity are
  separate identifiers and are never substituted for one another.
- Every distributed plugin carries a version-bound, machine-readable surface
  contract at a product-declared path. A product earns support independently
  on each exact surface.
- Adoption is product-local: Grove may retain its working SemVer machinery,
  while Trellis and every other adopter reconcile their own standing
  decisions before implementation.

**Open** (0):

- None.

**Parked** (0):

- None. Public directory submission, GitHub Release objects, and release-note
  automation are outside this contract; they require no decision until a
  product or host channel needs them.

## Context

`kodhama-0002` established one thin family install door while preserving
product-owned release cadence. The Claude and Codex catalogs now prove that
one repository can point at product-owned packages, but they do not establish
one package-release contract or one vocabulary for exact host surfaces.

Grove has already implemented the useful product half of this shape:
`plugins/grove/VERSION` is one host-neutral SemVer authority; its Claude and
Codex manifests carry the same value; `grove-v<VERSION>` identifies the
release commit; and `plugins/grove/surfaces.json` binds support evidence to the
same package version. Grove's matrix also contains Grove-only facts—such as
role-bridge state and its full role-discovery record—that do not belong in a
family schema.

Trellis deliberately chose a different package-version practice in
`trellis/decision-0036-plugin-versions-by-commit`: its plugin manifest omits a
SemVer value and the host resolves the package by commit. Trellis separately
uses a `payload@<hash>` stamp to identify rendered payload bytes. That is
useful provenance, but it demonstrates why the family needs distinct names
for a consumer-facing package release, its exact source, and any generated
content inside it.

Without a family minimum, catalogs cannot state which release they expose,
support matrices drift into incomparable product formats, and the presence of
a marketplace entry is easily mistaken for proof that the product works on
every surface where that marketplace can be reached.

## Decision

### 1. Every distributed plugin has one product-owned SemVer release

A **distributed plugin** is a product package listed in any canonical
Kodhama host catalog. Before listing, it shall have:

- exactly one product-owned canonical SemVer authority, at a path declared in
  the package's release metadata;
- the same value in every host manifest and every declared package-version
  carrier;
- an immutable repository tag named `<plugin>-v<version>` pointing at the
  exact release commit; and
- release validation that fails when the authority, a carrier, or the
  version-bound surface contract disagrees.

The authority may fit the product: Grove may retain its package-root
`VERSION`; Wisp may designate its existing `package.json`; Trellis may
introduce `VERSION`. The rule is one declared authority plus derived or
validated parity, not a duplicated filename. The product owns the value and
when to change it. Stewards does not coordinate one family-wide version or
release train: `grove@0.3.0` and `trellis@0.3.0` are unrelated releases.

The author of a release change proposes the SemVer level from its
consumer-visible effect; the product's own human release gate ratifies it:

- **patch** — a backward-compatible fix or evidence/provenance correction
  that adds no capability and withdraws no valid behavioral promise;
- **minor** — a backward-compatible capability or supported-surface addition;
  while the product is below `1.0.0`, a breaking change also occupies this
  slot by **Kodhama family convention**; and
- **major** — a breaking consumer contract change at or after `1.0.0`,
  including removal of a valid supported-surface promise.

SemVer itself says that `0.y.z` is for initial development and its public API
should not be considered stable; it does not prescribe “breaking equals
minor.” The latter is this family's explicit operational convention so that
pre-1.0 products make the same bump judgment.

Correcting a false support claim is never delayed to preserve a convenient
bump category. The product withdraws the claim loudly and selects the smallest
SemVer level that honestly communicates the compatibility impact.

### 2. The plugin public contract determines compatibility

A plugin's **public contract** is every consumer-observable promise whose
change can alter installation, invocation, configuration, managed project
state, or supported behavior. It includes:

- plugin and marketplace coordinates plus documented installation inputs;
- host-visible commands, skills, agents, hooks, connectors, and invocation
  names;
- configuration keys, accepted values, defaults, and migration behavior;
- files or managed blocks the plugin creates, changes, preserves, or removes;
- documented runtime/host requirements and exact-surface support promises; and
- any product-owned output or protocol that another tool or repository is
  expected to consume.

Internal refactors, unpublished test fixtures, and additional evidence for an
unchanged claim are not public-contract changes. A payload identity is part of
the public contract only when a consumer is expected to pin, compare, or
otherwise act on it. Products may declare additional public surfaces, but they
may not exclude an observable promise merely to avoid a version bump.

### 3. Four identities remain distinct and are bound at release

The family uses four separate terms:

| Identity | Meaning | Example |
|---|---|---|
| **package version** | Consumer-facing release and compatibility identity | `0.3.0` |
| **release tag** | Immutable repository ref for that package release | `grove-v0.3.0` |
| **source commit** | Exact source tree identified by the release tag | a full git commit id |
| **payload identity** | Byte/content identity of a generated or vendored component inside the package | `payload@0760a802ccd1` |

The release record binds all identities that exist for that product. A commit
id or payload hash remains valuable provenance, but neither replaces the
package version. A payload may change only through a package release once it
is distributed; the new release records the resulting payload identity.

### 4. Every plugin owns a version-bound surface contract

Each distributed plugin declares one machine-readable surface-contract path
in its release metadata. `surfaces.json` at the package root is the family
default and Grove's existing path, not a mandatory duplicate when a product
already has one canonical equivalent. Stewards publishes the common schema
and canonical surface registry; the product owns the file, its support claims,
and its evidence.

The common contract requires:

- `schema_version` and the adopted family contract version;
- `version`, equal to the value read from the plugin's declared canonical
  SemVer authority;
- rows keyed by canonical `surface_id`, with a host and one of
  `supported`, `candidate`, or `unsupported`;
- evidence paths or stable evidence references;
- an explicit load/use path and support record for `supported`;
- a missing capability and user-visible disclosure for `candidate` and
  `unsupported`; and
- no duplicate or unknown surface id.

Only `supported` is a support claim. `candidate` records an integration path
whose behavioral proof is incomplete; `unsupported` records no promise.
Absence of a row is also no support claim. Evidence from one exact surface
cannot satisfy another row.

The common schema is a minimum, not a universal product model. Products may
add namespaced or schema-declared extensions and stricter release rules.
Grove therefore retains its bridge states and role-discovery proof; Trellis
may record hook delivery, fallback, and live-rule behavior. Stewards never
promotes a product row or manufactures product evidence.

### 5. Support documentation derives from the product contract

A product's public support table and host-manifest support claims derive from,
or are mechanically checked against, its declared surface contract. A package
release fails before tagging when:

- a declared version carrier disagrees;
- the surface file has an unknown or duplicate id;
- a supported row lacks exact-surface evidence;
- a generated support table is stale; or
- product-specific extension validation fails.

Release validation proves the package and its claims are internally
consistent. It does not prove that a Stewards marketplace or cloud/CI
provisioner currently exposes the package; that is the separate distribution
availability contract, established independently from this package contract.

### 6. Existing nonconforming catalog stock has a bounded transition

The Claude catalog already lists Trellis, whose standing package-version
decision does not provide the canonical SemVer authority required here. That
entry may remain during the first implementation wave only as explicitly
disclosed **legacy published stock**:

- it is not family-contract conforming;
- it cannot be described as clean-install verified;
- it cannot contribute to an overall usable-surface claim; and
- every Stewards availability view identifies the missing release contract.

This is a migration seam, not grandfathering. The first implementation wave is
incomplete until Trellis adopts this contract and publishes a conforming
release or Stewards delists the entry. The same rule applies to any other
already-listed package found nonconforming during inventory; every such entry
is adopted or delisted in that wave, with no indefinite legacy state. New
entries receive no transition exception.

## Ownership boundary

| Owner | Owns |
|---|---|
| **Stewards** | SemVer/tag convention, common surface schema, canonical surface ids, and cross-product conformance fixtures |
| **Product** | Canonical authority and its path, version value, release timing, host manifests, surface rows, behavioral evidence, product extensions, product release validation |
| **Host catalog** | A pointer to a released product package; never the package version authority |

This standard centralizes the contract, not release judgment or implementation.

## Consequences and rollout

1. Stewards adds a versioned machine-readable surface registry, a common
   plugin-surface schema, and positive/negative conformance fixtures as part of
   the install door. The schema describes the common minimum and permits
   declared product extensions.
2. Grove records adoption in its own append-only decision graph. Its existing
   `VERSION`, dual-manifest equality, tag workflow, surface matrix, generated
   support table, and product validators remain the reference implementation;
   only family-contract metadata and shared-schema conformance are added.
3. Trellis makes a product decision that supersedes
   `decision-0036-plugin-versions-by-commit` for **package releases only**,
   introduces a declared SemVer authority and `<plugin>-v<version>`, and
   preserves its payload content stamp as a distinct identity.
4. Wisp and any later plugin make their own adoption decision before entering
   a family host catalog. A product that is not a distributed plugin owes no
   artificial plugin version.
5. Stewards inventories every existing Claude and Codex entry. Trellis is
   marked as disclosed legacy published stock until its conforming release
   replaces the mutable entry or the entry is delisted. The wave cannot close
   with legacy stock remaining.
6. Product adoption changes are independently reviewable and releasable. No
   product waits for a synchronized family release.

## Acceptance criteria

- **AC1:** The family schema distinguishes package version, release tag,
  source commit, and payload identity and contains fixtures that reject their
  substitution.
- **AC2:** A conforming product release declares one canonical SemVer
  authority, matches every declared carrier to it, creates an immutable
  `<plugin>-v<version>` tag, and binds a version-matched surface contract.
- **AC3:** A product matrix can retain product-specific fields without placing
  them in the family vocabulary.
- **AC4:** A supported row cannot pass common validation without exact-surface
  evidence and a support record; candidate, unsupported, and absent rows make
  no support claim.
- **AC5:** Grove adopts the contract without reimplementing its working
  `VERSION` machinery; Wisp may keep `package.json` as authority; and Trellis
  explicitly reconciles its conflicting package-version decision while
  preserving its payload identity.
- **AC6:** No catalog entry or provisioner state is accepted as behavioral
  support evidence.
- **AC7:** Every catalog entry present when this decision lands is either
  backed by a conforming product release or disclosed as temporary legacy
  published stock, and the first implementation wave cannot complete until
  every legacy entry is adopted or delisted.

## Self-check (gate)

The decision builds on approved `kodhama-0002` and does not consume draft
`kodhama-0013` as settled input; the latter is provenance only through
`informed_by`. It preserves independent product cadence and gives every
cross-product fact one Stewards home while keeping behavioral truth in each
product. Grove and Trellis are described from their actual standing records,
including their incompatible current package-version choices. The four
identities, support states, ownership boundary, propagation, and pass/fail
conditions are explicit. The plugin public contract is defined, and the
pre-1.0 breaking-as-minor rule is identified as family policy rather than
misattributed to SemVer. Existing nonconforming Trellis stock is surfaced with
a terminating migration condition. No current Claude, Codex, cloud, CI, or
SDK support is inferred. Promote `draft → gated`; `approved` remains a human
intent act.

## Approval record

On 2026-07-24 the maintainer directed the family SemVer/distribution strategy,
asked that it be applied across the plugin producers, and authorized merge
when independently sound. The decision-adversary returned SOUND after its
legacy-transition, public-contract, and SemVer-attribution findings were
folded. This `approved` status records that prior human intent act; it does not
turn any candidate or unavailable surface into support.
