---
id: kodhama-0023-separate-operational-availability-from-support
type: decision
status: gated
depends_on: [kodhama-0017-retire-family-release-certification, kodhama-0021-separate-adoption-posture-from-support, kodhama-0022-propagate-collective-strategy]
informed_by: [grove/discovery-surface-support-and-setup-eligibility]
owner: agent
updated: 2026-07-26
---

# Decision: separate operational availability from support

## Decision state

**Decided** (maintainer shaping, 2026-07-26):

- The family needs shared grammar that does not make a support claim decide
  whether a plugin can be installed, set up, or used.
- `candidate` will not remain a durable common support category.
- Every product-declared exact surface row will carry the two-field common
  grammar:
  - `availability_state: available | unavailable`; and
  - `support_claim: claimed | none`.
- The common grammar stops at those two fields and their invariants. Products
  continue to own paths, evidence, qualification, behavior, and validation.
- Grove will be the first product to apply the distinction through its own
  planner-dogfood setup work.
- After ratification, the strategy will propagate under decision 0022 through
  thin local receipts in Grove, Trellis, and Wisp. Retired Spore is excluded.
- The active Kodhama plugin in this repository follows the same grammar but
  needs no cross-repository receipt; its field migration remains separate
  product implementation.

**Open** (0):

- None.

**Parked** (4):

- The Kodhama plugin's product-specific migration of
  `plugins/kodhama/surfaces.json`.
- Grove's eligible rows, confirmation behavior, lifecycle operations,
  migration, validation, and tests.
- Trellis's product-specific migration from its current `behavior_state`
  model.
- Any Wisp metadata change; Wisp currently has qualification metadata but no
  project setup operation or support-state field.

## Context

Stewards decision 0021 established that adoption posture, distribution, and
support are distinct. A host-valid package may be distributed for disclosed
dogfood or preview before support, and support remains an affirmative,
product-owned public promise.

Grove then exposed a remaining coupling: its lifecycle permits setup only when
the exact surface is already marked `supported`. Its technically usable Codex
candidate and host-native Claude interactive rows therefore cannot be composed
for the planner dogfood that Grove has already approved.

This looks like collective grammar because the ambiguity is not Grove-specific:
“no support claim” does not mean “known not to work,” and technical
availability does not itself create a support promise. Trellis currently uses
a three-value behavioral surface state while independently deciding setup
feasibility. Wisp records qualification rather than support and has no project
setup operation. The active Kodhama plugin records exact surface rows without
either fact.

All four active plugin packages therefore expose machine-readable surface rows
but express these two cross-product facts differently or not at all. Shared
semantics with product-chosen carriers would preserve that translation burden
and allow the same conflation to recur under different field names. The
maintainer selected identical field names and closed values so a reader or
tool can interpret the two facts without product-specific mapping.

There is also a standing boundary to preserve. Decision 0015 formerly made a
common surface schema Stewards-owned, including
`supported | candidate | unsupported`. Decision 0017 superseded that
architecture in full and expressly returned surface contracts, product setup,
and support machinery to products. This decision deliberately restores only
two common row fields and their meanings. It leaves the discarded registry,
certification, release, evidence, and validator machinery retired.

## Decision

### 1. Operational availability and support are independent

For an exact host surface:

- **Operational availability** asks whether the product offers a bounded,
  disclosed way to install, set up, or use the plugin there.
- **Support claim** asks whether the product makes an affirmative,
  evidence-backed public reliability or compatibility promise there.

Operational availability may be present while no support claim exists. That is
the ordinary shape of disclosed dogfood or preview use. Conversely, no support
claim does not establish non-functionality; it records the absence of the
promise.

Operational availability does not imply support. A support claim requires
operational availability, but it does not create that availability: the
product must establish and record both facts. Catalog presence, installation
success, qualification progress, versioning, release tags, or an adoption
posture may not silently substitute for either fact.

### 2. `candidate` is not a durable shared support category

`candidate` may continue to describe transient package bytes, a release
candidate, or qualification work in a product's evidence. It does not sit
between “support claimed” and “no support claim” in the shared semantic model,
and it may not implicitly authorize or refuse a distinct product operation.

### 3. Exact surface rows use two common fields

Every machine-readable exact surface row declared by an active distributed
Kodhama plugin carries:

```json
{
  "availability_state": "available",
  "support_claim": "none"
}
```

The closed values are:

- `availability_state: available | unavailable`; and
- `support_claim: claimed | none`.

`available` means the product offers a bounded, disclosed operational path for
that exact surface. `unavailable` means it does not currently offer such a
path; it does not assert that operation is technically impossible.

`claimed` means the product makes an affirmative, evidence-backed public
support promise for that exact surface. `none` means no such claim exists; it
does not assert failure or non-functionality.

Three combinations are coherent:

| Availability | Support claim | Meaning |
|---|---|---|
| `available` | `claimed` | An operational path and a support promise both exist. |
| `available` | `none` | Disclosed dogfood or preview use can proceed without support. |
| `unavailable` | `none` | The product offers neither an operational path nor support. |

`unavailable + claimed` is invalid because a product cannot honestly promise
support while offering no operational path on the same exact surface.

The two fields are a common minimum. Products continue to own:

- surface rows and technical prerequisites;
- setup, refresh, installation, or use behavior;
- load paths, bridge state, and qualification state;
- disclosures, confirmation UX, and rollback;
- behavioral evidence and support promotion; and
- validation and tests.

A product may add fields suited to its own behavior. Stewards creates no
common surface registry, file path, evidence schema, transition engine,
cross-product validator, release gate, or certification service.

This partially supersedes only decision 0017's blanket exclusion of a
universal surface contract, narrowly permitting these two row fields and their
invariants. Every other retirement and product-ownership boundary in decision
0017 remains current.

### 4. Propagation

Once ratified, this strategy applies to the active Kodhama plugins:

- **Kodhama plugin:** the product package in this repository adopts the common
  fields through separate product implementation. It needs no thin receipt
  because this repository owns the upstream decision.
- **Grove:** receive the strategy, then separately decide and implement its
  exact support/setup model.
- **Trellis:** receive the strategy; any reconciliation of its current
  `behavior_state` metadata is a separate product decision.
- **Wisp:** receive the strategy as a constraint on future surface metadata;
  no current schema or setup change follows.

Spore receives no receipt because it is retired and has no current
distribution or surface model. Future plugin entrants catch up under decision
0022.

One conductor brief will track the three thin cross-link ADRs and their landed
links, plus the same-repository Kodhama plugin follow-up. Receipt communicates
the strategy but authorizes no product implementation, release, setup, or
support change.

## Rejected options

- **Keep `candidate | supported | unsupported` as the shared support ladder.**
  Rejected by the maintainer: it conflates incomplete qualification, absence
  of a support promise, and operational eligibility.
- **Make adoption posture the missing machine state.** Rejected by decision
  0021: dogfood, preview, and supported are reliance postures, not universal
  schema values or machine gates.
- **Share only the meanings and let products choose field names.** Rejected by
  the maintainer: every active plugin already has machine-readable exact
  surface rows, while their current carriers differ or omit these facts.
  Product-specific carrier translation would defeat the purpose of a common
  grammar and permit the same coupling under different names.

## Consequences

- Products can expose honest dogfood or preview paths without weakening the
  meaning of support.
- “No support claim” stops being misread as either a proven failure or a
  machine refusal.
- Qualification may still use candidate terminology without turning it into
  durable support grammar.
- Surface rows become comparable on the two facts that must not be conflated,
  while all operational details remain product-owned.
- Adopters owe a small field migration, but no common runtime or validator.
- The first rollout adds three thin receipts but no family registry,
  validator, or certification service.

## Acceptance criteria

- **AC1:** Operational availability and support are defined as independent
  product facts for an exact host surface.
- **AC2:** Operational availability without a support claim is explicitly
  valid for disclosed dogfood or preview.
- **AC3:** Absence of a support claim does not mean proven non-functionality
  and does not alone authorize or refuse a product operation.
- **AC4:** `candidate` is not a durable shared support category or an implicit
  operation gate.
- **AC5:** Adoption posture remains separate and follows decision 0021.
- **AC6:** Every active plugin's declared exact surface rows use
  `availability_state: available | unavailable` and
  `support_claim: claimed | none`; `unavailable + claimed` is invalid.
- **AC7:** Propagation targets Grove, Trellis, and Wisp through decision 0022;
  the same-repository Kodhama plugin is an explicit implementation follow-up,
  and retired Spore is excluded.
- **AC8:** Receipts authorize no product implementation, setup, release, or
  support change.
- **AC9:** Decision 0017 is superseded only enough to permit the two-field
  common grammar; no registry, file path, evidence schema, transition engine,
  cross-product validator, release gate, or certification service returns.

## Open questions

None.

## Self-check

The two fields encode distinct facts and the valid-combination table closes
the only incoherent pairing. `support_claim: claimed` avoids reusing decision
0021's `supported` adoption-posture value. `candidate` remains available for
transient qualification without becoming support grammar. Product-owned
evidence and behavior remain local, and decision 0017 is narrowed explicitly
rather than contradicted silently. The rollout covers all four active plugin
packages, follows decision 0022 for cross-repository receipts, and excludes
retired Spore. No open question remains, so the artifact stays `gated` for
fresh independent soundness review.

## Lifecycle record

This is the upstream shaping canvas requested after Grove selected an
independent support/setup architecture and asked whether the distinction was
collective grammar. Read-only audits covered the current Stewards boundary and
the live surface models in Grove, Trellis, Wisp, and retired Spore. On
2026-07-26 the maintainer selected a uniform two-field grammar while retaining
the minimal boundary around it. No product implementation or rollout memo is
part of this decision PR.
