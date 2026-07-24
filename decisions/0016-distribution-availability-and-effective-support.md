---
id: kodhama-0016-distribution-availability-and-effective-support
type: decision
status: superseded  # retired in full by kodhama-0017 (2026-07-24); original approval record remains in this file
depends_on: [kodhama-0002-delivery-channels, kodhama-0012-codex-marketplace-channel, kodhama-0015-family-plugin-release-and-surface-contract]
informed_by: [grove/adr-0029-non-interactive-loading, grove/adr-0031-multi-host-distribution, kodhama-0013-family-codex-native-product-support]
superseded_by: [kodhama-0017-retire-family-release-certification]
owner: agent
updated: 2026-07-24
provenance: maintainer direction on 2026-07-24 to make Stewards responsible for family marketplace availability and reusable headless/cloud provisioning while products retain their own surface contracts; artifact approval remains at the human ship gate
---

# Decision: Stewards owns distribution availability; effective support is derived, never declared by a catalog

> **Superseded by `kodhama-0017-retire-family-release-certification`
> (2026-07-24).** The shared availability, effective-support, cross-repository,
> and universal provisioner architecture is retired. This file remains the
> historical record of the earlier decision.

## Decision state

**Decided** (maintainer direction, 2026-07-24):

- Stewards owns the family host catalogs, their release pointers, and shared
  provisioning routes for local, headless/CI, and cloud/container surfaces.
- Products own package behavior and exact-surface support; marketplace
  presence and successful installation are not product support.
- Stewards records catalog availability and provisioner readiness as
  independent states with their own evidence.
- Effective support is the conjunction of matching distribution, product,
  consumer, and environment facts. It is computed, not stored as an
  independently editable claim.
- Generic provisioning may install the selected family plugin set for both
  Claude and Codex on one machine. It does not become a combined product,
  builder repo, or shared runtime.
- This capability partially supersedes `kodhama-0002`'s “no build logic”
  install-door boundary and the current repository description that limits the
  door to host-native manifests. The one canonical repository, thin-catalog,
  and product-owned package boundaries stand.

**Open** (0):

- None.

**Parked** (0):

- None. New hosts and public directories join only when their host-native
  channel exists; the registry can represent them as unavailable without
  inventing an implementation issue.

## Context

`kodhama-0002` and `kodhama-0012` establish one thin install repository with
host-native Claude and Codex catalogs. `kodhama-0002` describes that door as
“one thin repo, N entries, no build logic,” and this repository's current
instructions narrow it to the two host-native manifests. The current manifests
establish only these catalog facts:

- the Claude catalog contains Trellis and Grove source pointers; and
- the Codex catalog contains a Grove source pointer.

Those files do not prove a clean installation, a cloud/container setup path,
headless CI provisioning, or product behavior on every surface. Conversely, a
product may have exact-surface behavioral evidence while a hosted environment
has no supported way to acquire its marketplace before the agent starts.

Grove's `adr-0029` assigned Grove ownership of uniform non-interactive rollout
because no family provisioner existed. That correctly prevented consumers
from independently inventing divergent recipes, but the generic part applies
equally to Trellis and every later family plugin. Keeping that part in each
product would duplicate marketplace registration, authentication, caching,
and host setup logic. Moving it to Stewards preserves thin product packages
while keeping product-specific post-install setup in the product.

That move is a genuine expansion of the install door, not a reinterpretation
of “no build logic.” This decision authorizes bounded executable distribution
logic—schema validation and host-specific pre-agent provisioning—and partially
supersedes only that clause of `kodhama-0002`. It does not authorize product
builds, copied product content, a shared runtime, coordinated product releases,
or a general-purpose family CLI.

## Decision

### 1. Stewards owns three distribution records

The install door gains versioned machine-readable metadata for:

1. **Surface registry** — canonical host/surface ids and descriptive host
   metadata. It names surfaces; it does not claim a product works on them.
2. **Catalog availability** — which package source selector a host catalog
   exposes; only an immutable selector can name an exact release and become
   clean-host verified.
3. **Provisioner availability** — which reusable pre-agent route can install a
   selected plugin set on an exact surface, with its prerequisites and
   evidence.

The metadata lives with the install door, not in product repositories. It is
the machine-readable source for Stewards availability documentation and
provisioner selection.

### 2. Catalog and provisioner states do not use “supported”

To keep product behavior distinct, Stewards uses availability vocabulary.

A catalog record is:

- **absent** — no entry exists;
- **published** — the host-native catalog contains a syntactically valid
  source selector, but no immutable release identity or clean-install proof is
  claimed; or
- **verified** — a retained clean-host record proves discovery and
  installation of an exact package version/source identity selected
  immutably.

A provisioner route is:

- **unavailable** — no route is offered;
- **candidate** — a mechanism is identified or partially exercised, but its
  end-to-end pre-agent result is unproven; or
- **verified** — retained evidence proves the route idempotently provisions
  the requested exact package release before that host starts.

Only `verified` satisfies a distribution prerequisite. A repository/path
selector without an immutable ref can be only `published`: a point-in-time
observation cannot make that mutable selector identity-bound or verified. A
verified route therefore requires either a host catalog selector that names
an immutable release ref or a provisioner that acquires the exact release tag
or source commit independently of the mutable catalog. A missing record is
`absent` or `unavailable`, never implied availability. Evidence is scoped to
the exact host surface and provisioner version; it does not flow across
Claude/Codex, local/cloud, interactive/headless, or container/action rows.

This separates two facts that `kodhama-0012` coupled for its Grove-first
rollout. A valid host package may be catalogued and distribution-verified
while all of its product rows remain `candidate`, `unsupported`, or absent.
That state can support testing and staged delivery, but it produces no
effective-support claim. On approval, this decision supersedes only
`kodhama-0012`'s rule that catalog admission requires a product-supported
surface; its one-repository, host-native, thin-catalog, and product-owned
package boundaries stand.

### 3. Every verified route binds one product release; a mutable published pointer does not

For every catalog record, Stewards records:

- plugin name;
- host catalog and source selector;
- the product surface-contract location and contract version; and
- publication evidence.

For `verified`, the record additionally requires package version, release tag,
full source commit, an immutable selector or exact-release provisioner
acquisition, and retained clean-install evidence. Where a host manifest can
express an immutable release ref, the catalog uses it. Where it cannot, that
catalog record remains `published`; recording what its mutable pointer happened
to resolve once does not bind its future identity. An exact-release
provisioner may still become verified by bypassing that ambiguity and
acquiring the tag or commit directly. The host catalog never becomes the
package release authority.

A product release does not imply marketplace publication, and a mutable
catalog pointer does not reliably expose either the newest or a deliberately
older release. Stewards reports such a pointer only as `published`, with no
available-version or identity-binding claim.

### 4. One Stewards provisioner serves host-specific routes

Stewards supplies a reusable, idempotent provisioning capability that can be
called from:

- a CI pre-step before any Claude or Codex job;
- a cloud/container setup script before the hosted agent starts; or
- a local/bootstrap flow where host-native marketplace state is absent.

Its input is explicit: requested plugins and versions, target host or hosts,
surface id, and environment-owned authentication/configuration. On a machine
running both Claude and Codex, one invocation may provision both host-native
catalogs and the requested packages. It detects existing matching state and
converges it; it never silently upgrades to a different release.

The provisioner owns marketplace registration, package acquisition,
host-specific pre-launch installation, idempotency, and availability
evidence. It does not:

- select every family plugin without consumer intent;
- assert product behavior;
- run or replace a product's setup/refresh operation;
- copy product rules or role contracts into Stewards; or
- promise hosted support from a successful local/CI installation.

Products publish any required post-install setup interface in their own
package contract. Consumers or job definitions select the products and
authorize credentials/environment changes.

This provisioner and the machine-readable distribution records extend the
repository's third allowed category, the **install door**. They do not create
a fourth category. On approval, the repository instructions and README shall
describe the install door as host-native catalogs plus their distribution
metadata, validators, and bounded provisioner adapters.

### 5. Effective support is a conjunction

For plugin `P`, package version `V`, surface `S`, and consumer environment
`E`, an effective-support claim is true only when all of the following are
true:

1. `P@V` has a product-owned `supported` row for `S`, with exact-surface
   behavioral evidence;
2. the chosen immutable catalog or exact-release provisioner route is
   `verified` for `P@V` on `S` and resolves the same release tag/source
   commit;
3. the consumer explicitly selected `P@V`;
4. `E` satisfies the recorded authentication, trust, runtime, and
   pre-launch prerequisites; and
5. any product-owned post-install setup required by the supported row
   completed successfully.

In compact form:

`effective = product-supported ∧ distribution-verified ∧ identity-match ∧ consumer-selected ∧ environment-ready ∧ product-setup-complete`

This value is rendered from its sources and is never hand-maintained in a
third matrix. Any missing, candidate, unsupported, mismatched, or unavailable
input makes the effective claim false and identifies the failing owner.

## Ownership boundary

| Owner | Owns | Does not own |
|---|---|---|
| **Stewards** | canonical surface ids; Claude/Codex catalogs; catalog pointers; reusable provisioners; clean-install evidence; availability documentation | product builds, package behavior, product setup semantics, behavioral support promotion |
| **Product** | package/release; host manifests; surface matrix; behavioral evidence; setup/refresh; product disclosures | family catalog state, generic cloud/CI marketplace provisioning |
| **Consumer/environment** | selected plugin set; credentials; trust; job/container invocation; local policy | family or product support declarations |

For Grove, this boundary partially supersedes only `adr-0029` D4's assignment
of the **generic uniform rollout carrier** to Grove. Grove continues to own
its explicit behavioral load paths, bridge, launchers, setup, and support
evidence. Grove must record that partial supersession in its own append-only
decision graph rather than silently changing implementation.

## Consequences and rollout

1. Stewards implements the registry and schemas authorized by
   `kodhama-0015` plus a versioned availability record under the install-door
   surface. Generated documentation shows catalog and provisioner states
   separately from linked product support.
2. `kodhama-0002` receives a partial-supersession forward pointer limited to
   its “no build logic” clause. `CLAUDE.md` and `README.md` update their
   repository-scope description so the install door explicitly includes
   distribution metadata, validators, and bounded provisioner adapters while
   excluding product build logic and content.
3. Initial availability data mirrors only retained evidence. Existing
   mutable marketplace entries begin and remain `published`; they cannot
   become verified without changing to an immutable selector. An
   exact-release provisioner may independently become verified after a clean
   acquisition/install record. No cloud, headless, SDK, action, or container
   route begins verified by inference.
4. Stewards implements the Claude/Codex provisioning core once, with thin CI
   pre-step and cloud/container setup adapters. The same core accepts one or
   both hosts and an explicit product selection.
5. `kodhama-0012` receives the required partial-supersession forward pointer
   when this decision is approved. Catalogued-but-unsupported entries must
   disclose that state and cannot appear in an effective-support rendering.
   Trellis's nonconforming existing entry additionally follows
   `kodhama-0015`'s bounded legacy-stock transition and cannot be verified or
   effective before adoption.
6. Grove adopts the ownership split, keeps its product matrix, and removes no
   product-specific load/setup proof.
7. Trellis adopts the release/surface contract, then uses Stewards
   provisioning for headless/cloud tests. Its hook, fallback, live-rule, and
   refresh behavior remain Trellis evidence, not provisioner evidence.
8. Wisp and future plugins follow the same split when their own package and
   surface contracts exist. No catalog entry is added merely to satisfy a
   rollout checklist.
9. Catalog publication follows product release; provisioner verification may
   then proceed while behavioral support remains pending. An
   effective-support claim follows only after both independent proofs. These
   are separate review seams and may fail independently.

## Acceptance criteria

- **AC1:** The Stewards registry and availability records validate
  independently from every product surface matrix and use no behavioral
  `supported` state.
- **AC2:** Every catalog record names its source selector and product
  contract; `verified` additionally requires package version, release tag,
  source commit, and either an immutable host selector or an exact-release
  provisioner acquisition. A mutable repository/path selector remains
  `published` and carries no identity-binding claim.
- **AC3:** A clean-host record is required for `catalog: verified`, and an
  exact-surface pre-agent record is required for `provisioner: verified`.
- **AC4:** One provisioner invocation can explicitly select Claude, Codex, or
  both and converges the requested exact plugin versions without silently
  installing unselected family plugins or upgrading versions.
- **AC5:** Effective-support rendering fails closed and identifies whether
  product support, distribution, identity, consumer selection, environment,
  or product setup is missing.
- **AC6:** Grove's generic rollout ownership is reconciled by a product
  decision; Grove-specific behavior remains in Grove.
- **AC7:** Initial records make no cloud/headless/SDK/action/container claim
  without retained route-specific evidence.
- **AC8:** A catalogued and distribution-verified package with no supported
  product row remains visible for staged testing while effective support
  fails closed and discloses the missing product evidence.
- **AC9:** The Stewards implementation contains no product build, copied
  product payload, shared runtime, or release coordinator; repository
  instructions name only the bounded install-door expansion authorized here.
- **AC10:** Trellis and every other nonconforming pre-existing entry remain
  disclosed legacy published stock, never verified/effective, until adopted
  or delisted; the first implementation wave cannot close with any remaining.

## Self-check (gate)

The decision consumes approved `kodhama-0002`, approved `kodhama-0012`, and
merged gated `kodhama-0015`; it uses gated `kodhama-0013` only as non-flow
provenance.
It preserves `kodhama-0002`'s canonical-repository, thin-catalog, and
independent-product boundaries while explicitly superseding its prohibition
on bounded install-door logic. Catalog publication, clean installation,
product behavior, consumer selection, and environment readiness have distinct
owners and observable evidence. The effective-support conjunction prevents
any one of them from silently standing in for another. Existing catalog
entries are reported only as mutable published facts unless an immutable
selector or exact-release provisioner proves more; no mutable selector is
identity-bound and no untested surface is promoted. The bounded legacy-stock
transition prevents current Trellis availability from becoming an indefinite
exception. The rollout has product, catalog, provisioner, and verification
seams instead of an all-at-once family release. Promote `draft → gated`;
`approved` remains a human intent act.

## Approval record

On 2026-07-24 the maintainer assigned marketplace availability and reusable
headless/cloud provisioning to Stewards, required product behavior to remain
product-owned, and authorized the reviewed rollout. The decision-adversary
returned SOUND after mutable selectors were made publication-only and exact
release binding was limited to immutable catalogs or exact-release
provisioners. This `approved` status records that prior human intent act.
