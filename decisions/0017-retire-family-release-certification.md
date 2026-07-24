---
id: kodhama-0017-retire-family-release-certification
type: decision
status: approved  # maintainer explicitly directed the reset on 2026-07-24; independent adversary returned SOUND
depends_on: [kodhama-0002-delivery-channels, kodhama-0012-codex-marketplace-channel, kodhama-0015-family-plugin-release-and-surface-contract, kodhama-0016-distribution-availability-and-effective-support]
informed_by: [kodhama-spec-0001-family-plugin-release-and-distribution-metadata, kodhama-spec-0002-bounded-pre-agent-provisioner]
owner: agent
updated: 2026-07-24
provenance: "approved maintainer intent, 2026-07-24: retire the oversized family release-certification architecture while preserving only the future narrow goal (metadata recording where marketplaces were tested; a Stewards skill that adds Claude/Codex marketplace setup to CI)"
---

# Decision: retire family release certification; keep only narrow marketplace-test setup

## Decision state

**Decided** (approved maintainer intent, 2026-07-24):

- The family release-certification architecture established by
  `kodhama-0015` and `kodhama-0016` is retired.
- Stewards retains only a narrow future distribution goal:
  - metadata can record **which marketplace on which host a test exercised**;
    and
  - a generic Stewards skill can add Claude Code or Codex marketplace setup to
    CI before a product's own tests run.
- The metadata records test scope. It does not certify a release, marketplace
  availability, installation success, product behavior, or support.
- The skill owns generic host marketplace setup only. Products own plugin
  selection, installation when their test needs it, assertions, behavior,
  support claims, releases, and release evidence.
- Specs `kodhama-spec-0001` and `kodhama-spec-0002` are superseded and are no
  longer implementation inputs.

**Open** (0):

- None.

**Parked** (0):

- None. The narrow metadata and skill need a new small contract before
  implementation; their exact schema and interface are deliberately not
  designed in this reset decision.

## Context

The maintainer's source direction is:

> “retire the oversized family release-certification architecture while
> preserving only the future narrow goal (metadata recording where
> marketplaces were tested; a Stewards skill that adds Claude/Codex
> marketplace setup to CI).”

`kodhama-0015` began with a family-wide package release and surface contract.
It made Stewards responsible for common SemVer and tag rules, release identity,
surface schemas, registries, evidence, and cross-product conformance.

`kodhama-0016` expanded that contract into catalog and provisioner availability,
cross-repository adoption resolution, effective-support derivation, and common
local, CI, and cloud/container provisioning routes. Specs 0001 and 0002 then
made those obligations executable through release inventories and histories,
approval records, extension runtimes, filesystem/process auditing, product
repository resolvers, availability records, effective-result generation, and
a sealed host-neutral provisioner protocol.

That system is coherent as a certification architecture, but it is not the
small marketplace-testing aid now wanted from Stewards. Preserving it would
make the install-door repository own product release policy and runtime
machinery merely to answer the much smaller question “which marketplace did
this CI test use?” and to perform host-native marketplace registration.

The existing Claude and Codex catalogs remain authorized by
`kodhama-0002` and `kodhama-0012`. This decision narrows the additional
distribution machinery around them; it does not retire either marketplace.

## Decision

### 1. Decisions 0015 and 0016 are superseded in full

`kodhama-0015-family-plugin-release-and-surface-contract` and
`kodhama-0016-distribution-availability-and-effective-support` remain readable
as historical records but no longer govern current or future implementation.

Their derived specs are likewise non-current:

- `kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v2`; and
- `kodhama-spec-0002-bounded-pre-agent-provisioner@v3`.

No new work may claim conformance to those specs. A later narrow marketplace
metadata or CI-setup contract starts from this decision rather than amending
either superseded spec.

### 2. Retain only descriptive marketplace-test metadata

A product test or its retained evidence may record the host-native marketplace
coordinate or source that the test actually exercised. The record answers only
where the test obtained marketplace configuration.

It does not imply:

- that every marketplace route currently exposes the plugin;
- that a plugin installed successfully unless the product test separately
  proves and says so;
- that the plugin behaves correctly;
- that the product supports the host or test surface; or
- that a release is approved, reproducible, complete, or current.

Stewards may eventually define the smallest shared field shape needed to make
those records comparable. Until that contract is approved, this decision
authorizes the goal, not a schema.

### 3. Stewards may own one generic CI marketplace-setup skill

Stewards may eventually ship a skill that configures a caller-selected
marketplace for Claude Code or Codex in CI before the caller's tests run. Its
boundary is host-native marketplace setup from explicit caller inputs.

The skill does not select a product or plugin, decide what must be tested,
install arbitrary runtime dependencies, launch an agent, run product setup,
judge test results, or emit support and availability conclusions. Product
repositories own invocation, credentials and CI environment, plugin-specific
actions, assertions, and evidence retention.

Local workstations, general cloud/container bootstrapping, and a universal
pre-agent provisioner are outside this ownership. If a future caller needs one
of those, it requires its own evidence and decision rather than inheriting the
retired architecture.

### 4. The following family machinery is explicitly excluded

Stewards does not own or require a universal contract for:

- **SemVer and tags:** version authorities, carrier parity, bump judgment,
  tag naming, or tag-to-commit certification;
- **release inventories and history:** package inventories, append-only
  release histories, payload binding, or family release-engine interfaces;
- **release approval:** product release-gate records or approval references;
- **runtime sandboxing:** extension-validator runtimes, runtime digests,
  filesystem/process write audits, or sealed execution evidence;
- **cross-repository resolution:** product-adoption manifests, pinned product
  checkouts, local repository resolvers, or cross-repo release lookup; and
- **effective support:** surface registries and contracts, catalog/provisioner
  availability state, clean-install certification, support joins, or
  generated effective-support results.

Products remain free to own any of these mechanisms locally. This decision
removes the family mandate and Stewards ownership; it does not prohibit a
product from choosing the same mechanism for its own reasons.

### 5. Implementation retirement is a separate change

This artifact change records the reset, updates current indexes and scope
descriptions, and marks the two specs non-current. It intentionally does not
delete the already-landed distribution implementation.

The follow-up implementation PR owes:

1. removal of the release/surface/availability/effective-support schemas,
   records, fixtures, validators, generators, resolver, and tests under
   `distribution/`;
2. removal of the bounded provisioner core, adapters, schemas, fixtures,
   evidence/status documents, tests, and version authority under
   `distribution/`;
3. removal of the distribution-only CI workflow and the temporary quality-gate
   instructions, pinned product-repository prerequisites, and the now-legacy
   `.product-repositories/` ignore;
4. preservation of the canonical Claude and Codex marketplace manifests,
   followed later by a fresh narrow contract and implementation for
   marketplace-test metadata and the CI marketplace-setup skill; and
5. refresh of `distribution/repository-scope.md` and its generated `README.md`
   and `CLAUDE.md` derivatives so they no longer say the retired implementation
   remains pending removal.

The removal PR must inventory exact files before deleting them so it neither
damages the two canonical catalogs nor mistakes old implementation for a
contract to preserve.

## Consequences

- Stewards returns from product release certification to its thin install-door
  role.
- Product repositories again own their release identity, histories, approval
  acts, runtime validation, and support claims without a family schema.
- Existing implementation is legacy pending removal and must not attract new
  features or adopters.
- The retained future work is small and separately ratifiable: one descriptive
  metadata contract and one generic CI marketplace-setup skill.
- Decisions 0015/0016 and specs 0001/0002 remain in history with forward
  pointers so the expansion and its retirement stay auditable.

## Acceptance criteria

- **AC1:** Decisions 0015 and 0016 are `superseded` and point here without
  losing their historical bodies.
- **AC2:** Specs 0001 and 0002 are `superseded`, point here, and the spec index
  no longer presents them as implementation inputs.
- **AC3:** Current repository scope describes only host-native catalogs, the
  future marketplace-tested metadata, and the future generic CI setup skill.
- **AC4:** The decision explicitly excludes universal SemVer/tag, release
  history, approval, runtime-sandbox, cross-repository-resolver, and
  effective-support machinery.
- **AC5:** This artifact change deletes no distribution implementation and
  records the exact deletion and documentation-refresh categories owed by the
  follow-up removal PR.
- **AC6:** The maintainer's explicit reset direction and the independent
  `SOUND` judgment are recorded before promotion to `approved`.

## Open questions

None. The future metadata schema and skill interface belong to their own small
contract-authoring step.

## Self-check (gate)

The decision quotes the maintainer's approved intent, retires rather than
silently rewrites the two approved decisions, makes both derived specs
non-current, draws a positive boundary around the only retained goals, and
names the implementation debt without mixing deletion into this artifact PR.
The independent decision adversary returned `SOUND` after its one bounded
inventory finding was corrected.

## Lifecycle record

The maintainer explicitly directed this reset on 2026-07-24. That human intent
act, followed by the independent `SOUND` judgment, promotes this artifact from
`gated` to `approved`.
