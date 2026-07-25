---
id: kodhama-0019-spore-handoff-capsules
type: decision
status: approved  # maintainer approved the direction-only decision on 2026-07-25; Spore remains retired
depends_on: [kodhama-0001-family-delivery, kodhama-0002-delivery-channels, kodhama-0007-one-render-many-copiers, kodhama-0014-retire-spore]
informed_by: [kodhama-0012-codex-marketplace-channel, kodhama-0013-family-codex-native-product-support]
owner: agent
updated: 2026-07-25
provenance: maintainer direction 2026-07-25 that a future Spore should produce a bundle of selected Kodhama functionality for vendoring elsewhere, directed either through interactive conversation or a fixed design; refresh semantics explicitly deferred; maintainer approved this as a direction-only decision while keeping Spore retired.
---

# Decision: direct Spore toward portable handoff capsules

## Decision state

**Decided** (maintainer, 2026-07-25):

- **Spore's prospective function is a handoff capsule.** It produces a
  bounded, target-specific bundle of Kodhama functionality that can be
  vendored into another repository.
- A capsule may be selected interactively through conversation or emitted
  from a fixed, product-owned recipe. Both modes select from canonical,
  release-rendered product payloads; neither may have an LLM re-derive or
  author product content.
- Several Kodhama products or plugins may contribute functionality. The source
  products continue to own that functionality; Spore owns the selection,
  mechanical assembly, packaging, and handoff boundary.
- This is a new direction, not a continuation of the retired macOS
  Terminal/Claude Remote-Control machinery. It inherits no code, membership,
  delivery channel, or support claim from the retired Spore.
- **This is direction only. Spore remains retired** until a later decision
  explicitly readmits it with a concrete product contract and standing.

**Open** (0):

- None.

**Parked** (4):

- **Refresh semantics:** whether a germinated capsule remains
  provenance-linked for an explicit future diff/refresh or becomes permanently
  detached after vendoring. The maintainer explicitly deferred this choice.
- **Capsule contract:** manifest shape, payload rules, provenance fields,
  target placement, conflict handling, and germination/apply behavior.
- **Implementation and delivery:** repository reuse, CLI versus plugin
  surfaces, supported hosts, marketplace presence, release policy, and
  migration or disposal of the retired session machinery.
- **Product identity and migration:** whether the new concept may reuse the
  old repository or `spore@kodhama` coordinate. Reuse must not silently update
  installed Terminal-era users into an unrelated product; a later decision
  must choose a distinct identity or an explicit breaking migration.

## Direction

Spore is the artifact dispersed as much as the mechanism that prepares it:
a portable handoff capsule containing a deliberately bounded selection of
Kodhama functionality for a specific destination.

The common operation is:

1. A user conversation or fixed recipe identifies a source capability, an
   enumerable canonical variant, and a target repository.
2. Spore mechanically selects, copies, patches managed blocks, and verifies
   only the release-rendered material required for that target. Interaction may
   resolve target-owned values but may not compose product-owned content.
3. Spore emits a reviewable bundle with enough provenance and manifest data to
   explain and verify where each part came from.
4. The bundle is vendored into the target, where its files become local
   project material rather than a runtime dependency on the source product.

Examples include a bounded Grove workflow handed to an unrelated project, a
Trellis governance posture prepared for local ownership, or a cross-product
context/specification capsule for independent continuation. These are examples
of one function, not separate Spore products.

## Product boundary

Spore does not own the capabilities inside a capsule. Grove, Trellis, Wisp,
and later products retain their own contracts, canonical payloads, and release
authority. Spore owns the cross-product operation that mechanically selects
and packages those payloads into a target-specific, inspectable handoff.

For Grove specifically, Spore may package an explicit workflow handoff but
does not take ownership of task routing, workflow stages, agent roles, or run
resumption. Those remain Grove operating-model concerns.

This direction is distinct from:

- **marketplace installation**, which installs a product-owned package and
  preserves that package as the operational dependency;
- **generic project scaffolding**, which creates a project shape without
  selecting a bounded Kodhama capability for handoff;
- **agent or session orchestration**, which drives running work rather than
  producing a vendorable artifact; and
- **the retired Spore implementation**, whose Terminal automation addressed a
  narrow Claude Remote-Control workflow.

The phrase **runtime-detached** is decided: using the vendored material must
not require a running Spore service or the source product at runtime. Whether
the material remains *provenance-linked* for optional maintenance is parked.

## Consequences

- `kodhama-0014`'s retirement remains in force. A later decision must
  explicitly readmit Spore; this direction decision does not do so.
- The name now has a recorded problem/function direction, but no implementation
  is authorized and no delivery claim is created.
- Product-specific recipes may eventually make capsule production
  deterministic; interactive selection may cover one-off targets. Both must
  converge on the same future capsule contract and mechanical-writer rules
  rather than create unrelated output formats or content-authoring paths.
- Any implementation proposal must demonstrate a real handoff use case and
  show why ordinary plugin installation or direct vendoring is insufficient.

## Acceptance criteria for this direction decision

- **AC1:** Spore is defined as producing bounded, target-specific, vendorable
  handoff capsules of Kodhama functionality.
- **AC2:** Interactive selection and fixed product-owned recipes are both
  valid input modes for the same conceptual output; neither authors or
  re-derives product payload content.
- **AC3:** Source products retain ownership of their functionality; Spore owns
  only selection, mechanical assembly, packaging, provenance, and handoff.
- **AC4:** Runtime detachment is required, while refresh/linkage semantics
  remain explicitly deferred.
- **AC5:** The retired session machinery, family readmission, implementation,
  and delivery are not implied by this direction.

## Self-check

This decision records the maintainer's chosen direction without inventing the
deferred refresh policy or reversing `kodhama-0014`. It distinguishes the
concept from standing marketplace and product-ownership decisions, gives both
selection modes one output boundary, conforms to `kodhama-0007` by forbidding
content-authoring writers, and leaves implementation contingent on a forcing
case. There are no open decision items. Promote `draft → gated` and route to
independent decision-adversary review before recording the maintainer's
approval in lifecycle status.

## Lifecycle record

The maintainer approved this as a direction-only decision on 2026-07-25 and
explicitly kept Spore retired. Independent decision-adversary re-review found
the reconciled decision `SOUND` at commit `67fc2ee`; the subsequent PR merge is
the delivery act, not a readmission or implementation authorization.
