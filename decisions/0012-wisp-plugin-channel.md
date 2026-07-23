---
id: kodhama-0012-wisp-plugin-channel
type: decision
status: gated
depends_on: [kodhama-0001-family-delivery, kodhama-0002-delivery-channels]
owner: agent
updated: 2026-07-23
provenance: maintainer direction 2026-07-23 — distribute all kodhama utilities through the common marketplace in kodhama/stewards; then "Do it all" while preserving dual Claude / Codex distribution, with permission to amend specs or supersede decisions in favor of the lowest-friction working design
---

# Decision: wisp gains a plugin channel with a built-in MCP surface

**Decision.** Wisp joins the canonical `@kodhama` marketplace as
**`wisp@kodhama`**, sourced from `kodhama/wisp` → `plugins/wisp/`. This amends
the Wisp channel recorded in `kodhama-0002` §4 and its channel matrix: npm/npx
is no longer the only intended zero-install surface. The plugin is the
low-friction agent-facing channel; Wisp's product repo remains the authority
for its runtime and any CLI channel it chooses to retain.

## Ownership boundary

- **Wisp owns the exact seven-file plugin payload**: runtime bundle, skill,
  Claude manifest and MCP configuration, Codex manifest with its inline MCP
  definition, documentation, and qualification record. Wisp also owns the
  product-side tests, versions, and release compatibility; those verification
  sources are not part of the installed payload. The marketplace must not copy
  or reinterpret either.
- **Stewards owns only discovery and routing**: one `git-subdir` pointer in
  `.claude-plugin/marketplace.json`, plus this cross-collective decision and
  the conductor ledger.
- **The catalog is not duplicated by host.** Stewards keeps its canonical
  `.claude-plugin/marketplace.json` as the one collective install door. The
  payload reached through that entry carries both host manifests, so Claude
  and Codex integration can evolve together from one product-owned artifact
  rather than two marketplace implementations.

## Runtime and install model

The plugin is installed **per user**, matching the marketplace's existing
plugin model. Installing it does not create a machine-global Wisp instance,
daemon, or shared mutable service.

Each participating agent session starts its own product-provided MCP process.
That process binds immutably to the project bus selected for that session;
individual tool calls and events carry their own run identifiers. Multiple
sessions can therefore observe the same project bus without implying multiple
machine-level “Wisps”; they are short-lived clients of project-bound state,
not singleton installations.

The built-in MCP server exposes Wisp's agent observability operations through
the standard tool boundary. This keeps host configuration thin: installation
delivers the executable payload and the definitions needed to launch it, with
no separate global CLI install or dependency-fetch step required at session
startup.

## Marketplace shape

Stewards adds one entry, causally ordered after grove and before the peripheral
spore tool:

```json
{
  "name": "wisp",
  "source": {
    "source": "git-subdir",
    "url": "kodhama/wisp",
    "path": "plugins/wisp"
  }
}
```

The product payload must exist and pass its independent Wisp-side gates before
this pointer merges. Merge order is therefore **Wisp first, Stewards second**;
the marketplace must never advertise a subdirectory that is absent from
Wisp's default branch.

## Consequences

- One per-user marketplace install makes Wisp available to both supported
  agent hosts; project setup should require an explicit project root only
  where the host cannot infer one safely. Run identity remains a tool/event
  input rather than process configuration.
- The Wisp repo may replace legacy delivery or implementation details when
  they add friction and have no useful compatibility value. This decision
  preserves the cross-collective boundary and dual-host outcome, not legacy
  internals.
- Remote or machine-wide Wisp services are not part of this channel. A future
  shared daemon or hosted transport would need its own decision because it
  changes trust, lifecycle, and state ownership.
- Stewards does not validate Wisp protocol semantics. It verifies only that
  the product-owned plugin root exists at the declared path and is installable
  through the catalog after Wisp lands.

## Acceptance criteria

- **AC1** `kodhama/wisp` default branch contains `plugins/wisp/` with both
  Claude and Codex manifests, a self-contained MCP-capable runtime, and the
  product-side verification required by Wisp.
- **AC2** Stewards' marketplace contains exactly one Wisp entry, pointing by
  `git-subdir` to `kodhama/wisp` → `plugins/wisp`, ordered
  `trellis · grove · wisp · spore`.
- **AC3** A clean per-user Claude install and a clean per-user Codex install
  can discover the shipped Wisp tools without a separate global Wisp install
  or dependency download at session startup.
- **AC4** Two independent sessions can bind to a project bus without a
  singleton daemon, while an unresolved project root fails safely instead of
  silently observing another project; run identity remains event-scoped.
- **AC5** The conductor brief records product and marketplace gates separately,
  merges Wisp before Stewards, and leaves any unrun install/host smoke visibly
  pending.

## Self-check (gate)

This decision follows `kodhama-0001`'s product-owned delivery / thin shared
surface boundary and `kodhama-0002`'s one-marketplace principle. It expressly
amends 0002's Wisp channel rather than editing that approved artifact. The
maintainer authorized the channel, implementation breadth, dual-host outcome,
and freedom to discard unhelpful legacy; the remaining gate is empirical:
the product payload and both host installs must pass before human merge.
`draft → gated`; `approved` = maintainer merge after the cross-repo checklist
is satisfied.
