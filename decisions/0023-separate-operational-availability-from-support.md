---
id: kodhama-0023-separate-operational-availability-from-support
type: decision
status: draft
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
- Grove will be the first product to apply the distinction through its own
  planner-dogfood setup work.
- After ratification, the strategy will propagate under decision 0022 through
  thin local receipts in Grove, Trellis, and Wisp. Retired Spore is excluded.

**Open** (1):

- Whether Stewards owns only the semantic distinction, leaving machine field
  names and enforcement product-owned, or reinstates a mandatory family
  surface schema by partially reversing decision 0017.

**Parked** (4):

- Grove's exact `setup_state` / support carrier, eligible rows, confirmation
  behavior, lifecycle operations, migration, validation, and tests.
- Any Trellis metadata migration from its current `behavior_state` model.
- Any Wisp metadata change; Wisp currently has qualification metadata but no
  project setup operation or support-state field.
- Shared schemas, registries, cross-product validators, transition engines,
  or support certification unless the maintainer deliberately chooses the
  machine-schema option above.

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
setup operation.

There is also a standing boundary to preserve. Decision 0015 formerly made a
common surface schema Stewards-owned, including
`supported | candidate | unsupported`. Decision 0017 superseded that
architecture in full and expressly returned surface contracts, product setup,
and support machinery to products. A shared semantic rule fits that reset; a
mandatory JSON schema would intentionally reverse part of it.

## Working proposal

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

Neither fact implies the other. Catalog presence, installation success,
qualification progress, versioning, release tags, or an adoption posture may
not silently substitute for either fact.

### 2. `candidate` is not a durable shared support category

`candidate` may continue to describe transient package bytes, a release
candidate, or qualification work in a product's evidence. It does not sit
between “support claimed” and “no support claim” in the shared semantic model,
and it may not implicitly authorize or refuse a distinct product operation.

### 3. Products own carriers and behavior

Under the proposed minimal boundary, this decision would define concepts and
invariants, not required JSON fields. Each product would continue to own:

- whether it needs machine-readable availability or support carriers;
- the carrier names, schema, and exact states;
- surface rows and technical prerequisites;
- setup, refresh, installation, or use behavior;
- disclosures, confirmation UX, and rollback;
- behavioral evidence and support promotion; and
- validation and tests.

A product that records both facts shall keep them independently readable and
shall not use the absence of a support claim as the sole reason to refuse an
otherwise product-authorized operation.

This preserves decision 0017's rejection of universal surface contracts,
registries, and certification machinery. Choosing a mandatory shared schema
instead would require an explicit, narrow partial supersession of that
decision.

### 4. Propagation

Once ratified, this strategy applies to the active Kodhama plugins:

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
links. Receipt communicates the strategy but authorizes no product
implementation, release, setup, or support change.

## Rejected options

- **Keep `candidate | supported | unsupported` as the shared support ladder.**
  Rejected by the maintainer: it conflates incomplete qualification, absence
  of a support promise, and operational eligibility.
- **Make adoption posture the missing machine state.** Rejected by decision
  0021: dogfood, preview, and supported are reliance postures, not universal
  schema values or machine gates.

## Consequences

- Products can expose honest dogfood or preview paths without weakening the
  meaning of support.
- “No support claim” stops being misread as either a proven failure or a
  machine refusal.
- Qualification may still use candidate terminology without turning it into
  durable support grammar.
- Under the working proposal, products remain free to choose minimal carriers
  suited to their actual operations.
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
- **AC6:** The final ownership choice explicitly preserves or narrowly
  supersedes decision 0017.
- **AC7:** Propagation targets Grove, Trellis, and Wisp through decision 0022;
  retired Spore is explicitly excluded.
- **AC8:** Receipts authorize no product implementation, setup, release, or
  support change.

## Open questions

The one live ownership question is maintained in `## Decision state`.

## Lifecycle record

This is the upstream shaping canvas requested after Grove selected an
independent support/setup architecture and asked whether the distinction was
collective grammar. Read-only audits covered the current Stewards boundary and
the live surface models in Grove, Trellis, Wisp, and retired Spore. No product
implementation or rollout memo is part of this draft.
