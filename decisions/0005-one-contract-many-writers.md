---
id: kodhama-0005-one-contract-many-writers
type: decision
status: gated
depends_on: [kodhama-0002-delivery-channels]
owner: agent
updated: 2026-07-08
provenance: maintainer, 2026-07-08, during the live plugin smoke — "would it make sense for the non-destructive path of the trellis CLI simply run the plugin install... wait, that's claude code only"; resolved as the inverse delegation, to act on family-wide from the conductor seat.
---

# Decision: one contract, many writers — delegation flows toward the deterministic writer

**Decision.** When a family product's install/compose artifact has more
than one writer (a deterministic binary, an agentic plugin skill, a
documented manual path), the rules are:

1. **The artifact contract is the source, not any writer.** The bundle
   format + version stamp is declared once; every writer names itself a
   derivative of it (decision-0028's derived-pairs rule, applied to
   delivery). Writers stay in sync *by contract*, never by code-sharing.
2. **Delegation flows only toward the deterministic writer.** An
   agentic writer (plugin skill) checks for the binary and delegates to
   it when present; a binary NEVER shells out to a harness-specific
   channel (that would invert its reason to exist: zero-prereq,
   any-harness). The maintainer's own catch, ratified.
3. **Every writer stamps the same version format** so staleness checks
   read uniformly regardless of which writer composed the overlay.

**Application today:** trellis — `/trellis:setup` gains the
delegate-to-binary step (its own PR, executed with this decision);
grove — already conforming (no binary by decision; canonical
`.claude/agents/` is the declared source, plugin payload carries sync
headers, both writers stamp `grove plugin@<sha>`); wisp — n/a until a
CLI exists; future tools inherit.

## Acceptance criteria

- **AC1** `/trellis:setup` run on a machine with the binary delegates
  (composes nothing by hand); without it, composes the identical bundle.
- **AC2** Both trellis writers name the bundle contract as their source
  in their own text.
- **AC3** No family binary ever invokes a harness-specific install
  channel.

## Self-check (gate)

Maintainer intent quoted; the rejected direction (CLI→plugin) recorded
with its reason; grove's conformance verified against its shipped
payload rather than assumed; ACs pass/fail. Promote `draft → gated`.
`approved` = human merge — deliberately left for the maintainer's own
read, as this rules how the family ships.
