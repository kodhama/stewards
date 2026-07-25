---
id: kodhama-0019-spore-handoff-capsules
type: decision
status: gated
depends_on: [kodhama-0001-family-delivery, kodhama-0002-delivery-channels, kodhama-0014-retire-spore]
informed_by: [kodhama-0012-codex-marketplace-channel, kodhama-0013-family-codex-native-product-support]
owner: agent
updated: 2026-07-25
provenance: maintainer direction 2026-07-25 that a future Spore should produce a bundle of specific Kodhama functionality for vendoring elsewhere, composed either through interactive conversation or a fixed design; refresh semantics explicitly deferred; maintainer approved this as a direction-only decision while keeping Spore retired.
---

# Decision: direct Spore toward portable handoff capsules

## Decision state

**Decided** (maintainer, 2026-07-25):

- **Spore's prospective function is a handoff capsule.** It produces a
  bounded, target-specific bundle of Kodhama functionality that can be
  vendored into another repository.
- A capsule may be composed interactively through conversation or emitted
  from a fixed, product-owned design.
- Several Kodhama products or plugins may contribute functionality. The source
  products continue to own that functionality; Spore owns the selection,
  composition, packaging, and handoff boundary.
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
  target adaptation, conflict handling, and germination/apply behavior.
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

1. A user or fixed recipe identifies a source capability and target
   repository.
2. Spore selects and adapts only the material required for that target.
3. Spore emits a reviewable bundle with enough provenance to explain where
   each part came from.
4. The bundle is vendored into the target, where its files become local
   project material rather than a runtime dependency on the source product.

Examples include a bounded Grove workflow handed to an unrelated project, a
Trellis governance posture prepared for local ownership, or a cross-product
context/specification capsule for independent continuation. These are examples
of one function, not separate Spore products.

## Product boundary

Spore does not own the capabilities inside a capsule. Grove, Trellis, Wisp,
and later products retain their own contracts and release authority. Spore
owns the cross-product operation that turns selected capability into a
target-specific, inspectable handoff.

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
  deterministic; interactive composition may cover one-off targets. Both must
  converge on the same future capsule contract rather than create unrelated
  output formats.
- Any implementation proposal must demonstrate a real handoff use case and
  show why ordinary plugin installation or direct vendoring is insufficient.

## Acceptance criteria for this direction decision

- **AC1:** Spore is defined as producing bounded, target-specific, vendorable
  handoff capsules of Kodhama functionality.
- **AC2:** Interactive composition and fixed product-owned recipes are both
  valid input modes for the same conceptual output.
- **AC3:** Source products retain ownership of their functionality; Spore owns
  only the composition, packaging, provenance, and handoff boundary.
- **AC4:** Runtime detachment is required, while refresh/linkage semantics
  remain explicitly deferred.
- **AC5:** The retired session machinery, family readmission, implementation,
  and delivery are not implied by this direction.

## Self-check

This decision records the maintainer's chosen direction without inventing the
deferred refresh policy or reversing `kodhama-0014`. It distinguishes the
concept from standing marketplace and product-ownership decisions, gives both
composition modes one output boundary, and leaves implementation contingent
on a forcing case. There are no open decision items. Promote `draft → gated`
and route to independent decision-adversary review before recording the
maintainer's approval in lifecycle status.
