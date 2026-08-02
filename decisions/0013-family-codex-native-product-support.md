---
id: kodhama-0013-family-codex-native-product-support
type: decision
status: approved  # maintainer intent act 2026-08-02, in session: "I would say approve them" — an in-PR flip recording that act, per grove/charters/lifecycle.md's gated -> approved mover rule; the merge performs the ship. Content re-read on flip 2026-08-02 and still live: trellis#220 is executing this decision's Codex-distribution mandate.
depends_on: [kodhama-0001-family-delivery, kodhama-0002-delivery-channels, kodhama-0008-family-inheritance-restate-nothing, kodhama-0012-codex-marketplace-channel]
superseded_in_part_by: [kodhama-0028]  # 2026-08-02 kodhama-0028 amends exactly two clauses: (a) "Each user-facing product MUST gain a Codex-native surface; trellis, grove, and wisp are the initial REQUIRED products" becomes a named intent with no schedule and no required tranche; (b) "in parallel with its existing Claude Code support" no longer obliges a Codex counterpart to a Claude-path change, so divergence between the two is expected rather than a defect. The DIRECTION of this record is unchanged and is not superseded.
owner: agent
updated: 2026-07-24
provenance: maintainer request 2026-07-24 to make native Codex support, preferably through plugin distribution, a product-family standard; initial named products trellis, grove, and wisp. Reconciled 2026-07-24 with merged grove#134 (dual-host Grove distribution) and merged stewards#9 / kodhama-0012 (the Grove-first Codex marketplace catalog). Maintainer merge of PR #11 preserved this record as a draft; the author self-check below promotes it to the execution-ready gate without claiming human approval.
---

# Decision: native Codex support becomes a product-family standard

> **Spore follow-up (2026-07-24):** `kodhama-0014-retire-spore` settles this
> decision’s parked Spore question by retiring the tool from the family. The
> Trellis/Grove/Wisp Codex mandate is unchanged.

## Decision state

**Decided** (maintainer request, 2026-07-24):

- Native **Codex** support is a delivery target for every user-facing Kodhama
  product, in parallel with its existing Claude Code support.
- **Codex plugin distribution** is the preferred delivery mechanism. At
  minimum, the initial Codex-plugin delivery tranche is **trellis**, **grove**,
  and **wisp**.
- Product bundles and their releases remain owned by their individual product
  repos. The stewards may provide one family marketplace/discovery surface;
  it does not become a builder repo or a shared runtime.
- `kodhama-0012-codex-marketplace-channel` / stewards#9 supplies the shared
  Codex marketplace catalog, initially for Grove only. It is the first catalog
  delivery, not a declaration that Trellis and Wisp are already listed.
- **Spore is deferred** from the initial Codex-plugin tranche (maintainer,
  2026-07-24). No Spore Codex package, catalog entry, or support claim is
  authorized here; its current Terminal session-driver machinery is neither
  extended nor retired by this decision.

**Open** (0):

- None.

**Parked** (1):

- **Spore’s purpose and standing:** decide separately whether Spore remains a
  steward; whether it should instead serve a broader dispersion/germination
  role outside the main forest; and whether its narrow Terminal session-driver
  machinery should retire. That decision may retain Spore as a Claude-only
  steward, retire it, or redefine it. `kodhama-0010`/`0011` currently define
  and package the Terminal machinery, so it must explicitly reconcile their
  membership, enumeration, channel, and migration consequences rather than
  silently redefine or remove it.

## Decision

The Kodhama product family adopts **native Codex support** as a standard
delivery channel, alongside—not in place of—Claude Code support. Each
user-facing product must gain a Codex-native surface; **trellis**, **grove**,
and **wisp** are the initial required products.

The preferred surface is a **Codex plugin**: a product-owned bundle with the
required `.codex-plugin/plugin.json` manifest and any product-appropriate
skills, MCP configuration, connectors, or hooks. A plugin must expose only
the capabilities its product actually needs; Codex support does not require
inventing a plugin-shaped feature for a product that has none.

Native support and plugin distribution are related but distinct completion
claims. A product has native Codex support when its intended behavior has been
exercised on a supported Codex surface using Codex-native configuration—for
example, project-wide instructions in `AGENTS.md`. Codex plugin distribution
is the preferred reusable delivery form where the product has a distributable
bundle; it requires its own manifest, marketplace metadata, installation, and
fresh-session verification. The former must never be relabelled as the latter.

### Grove delivery, and the family follow-on

Merged [grove#134](https://github.com/kodhama/grove/pull/134) is the initial
product implementation. It adds Grove's native Codex package, generated
dual-host projections, lifecycle operations, release checks, and a
surface-specific support record. Its supported Codex claim is deliberately
bounded to non-ephemeral `codex exec`; it does not imply support for every
Codex host surface.

Merged [stewards#9](https://github.com/kodhama/stewards/pull/9) is the
corresponding thin catalog delivery. It creates
`.agents/plugins/marketplace.json` in the existing `kodhama/stewards` install
repository and initially points only to Grove's product-owned package. Its
gated decision, `kodhama-0012-codex-marketplace-channel`, is already the
authoritative decision for this catalog shape. This decision neither duplicates
nor supersedes it: it makes the resulting native-Codex posture a family
standard and governs the Trellis and Wisp follow-ons.

The collective keeps the family’s existing delivery topology. Each product
builds, versions, and publishes its own plugin in its own repository. The
stewards’ install door may host one Codex-native marketplace at
`.agents/plugins/marketplace.json`, listing those independently owned bundles
as the family discovery and installation surface. This is a catalog, not a
combined product or a release dependency.

This decision does not alter existing Claude Code channels. Where a single
underlying skill or workflow can serve both hosts, the product may share it;
each host’s manifest, marketplace metadata, installation path, and lifecycle
behavior must remain valid in that host rather than treating Claude
compatibility as native Codex support. A later Spore purpose decision governs
any change to Spore's Claude-specific channel.

## Scope and boundaries

- **In scope:** every user-facing product, beginning with Trellis, Grove, and
  Wisp; product-specific Codex plugin bundles; the family marketplace catalog
  established by `kodhama-0012`.
- **Out of scope:** a monorepo or builder; a common runtime; retiring Claude
  Code support; claiming a Codex distribution channel works before it has been
  installed and exercised on a supported Codex surface.
- **Not automatically included:** the design system and Homebrew tap, which
  have no independent user-facing Codex workflow. **Spore is deferred**:
  it is a Claude-specific steward tool, not a tree/product; this decision
  authorizes no Codex surface for it, and its future purpose is parked for a
  separate decision.

## Why

`kodhama-0001` and `kodhama-0002` already establish independent product
delivery with a thin collective install surface. `kodhama-0012` applies that
shape to Codex and Grove#134 proves the first product package and supported
surface. Extending the posture to Trellis and Wisp lets the family meet Codex
users where they work without changing product ownership or coupling releases.

## Acceptance criteria

- **AC1:** Trellis, grove, and wisp each ship a valid Codex plugin manifest in
  their own repository and document their Codex installation and use path.
- **AC2:** A Codex user can discover, install, and use each initial-tranche
  plugin in a fresh supported Codex session from the family marketplace or a
  documented product-owned equivalent.
- **AC3:** The Codex marketplace records the required installation policy,
  authentication policy, and category for every listed plugin.
- **AC4:** No product advertises native Codex support until AC2 has been
  exercised for that product.
- **AC5:** This decision makes no change to an existing Claude Code channel;
  any change to Spore's channel is governed only by its later purpose decision.

## Evidence

- **Codex plugin distribution (verified, 2026-07-24):** OpenAI’s *Build
  plugins* documentation specifies the native `.codex-plugin/plugin.json`
  manifest, a repo marketplace at `.agents/plugins/marketplace.json`, and
  Git-backed marketplace entries. [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- **Supported surfaces (verified, 2026-07-24):** OpenAI’s *Plugins*
  documentation says Codex in the ChatGPT desktop app and Codex CLI can browse
  and use plugins, while the IDE extension cannot. [Plugins](https://learn.chatgpt.com/docs/plugins)
- **Grove product implementation (verified, 2026-07-24):** merged
  [grove#134](https://github.com/kodhama/grove/pull/134) adds a native Codex
  package and reports support evidence for its bounded
  `codex-exec-non-ephemeral` surface.
- **Family catalog (verified, 2026-07-24):** merged
  [stewards#9](https://github.com/kodhama/stewards/pull/9) carries gated
  `kodhama-0012-codex-marketplace-channel`, adds the host-native catalog, and
  initially lists only Grove. It keeps product code and releases in product
  repositories.

## Self-check (draft)

The decision preserves the family’s already-ratified polyrepo and thin-shared-
surface model (`kodhama-0001`/`0002`). Codex-specific claims were verified
against current OpenAI documentation rather than inferred from the existing
Claude marketplace. Grove#134 and stewards#9 are described at their actual,
separate scopes: a product-owned dual-host package and a thin, Grove-first
catalog. This draft extends that established direction to the family rather
than creating a competing marketplace decision.
Spore’s initial-tranche status is resolved as deferred. Its possible
redefinition or retirement is explicitly parked because it would amend
`kodhama-0010` and `kodhama-0011`, including their membership and delivery
consequences, rather than merely refine this delivery decision.

## Lifecycle record

PR #11 explicitly introduced this record as a draft, so its maintainer merge
is not treated as ratification. On 2026-07-24 the author rechecked the record
against approved `kodhama-0001`, `kodhama-0002`, `kodhama-0008`, and
`kodhama-0012`, plus the merged Grove implementation evidence named above.
Its dependencies are settled, its decided/open/parked state is explicit, and
its claims remain bounded to the named products and verified host facts.
That self-check promotes `draft → gated`; human approval remains open.

**Approved 2026-08-02.** The maintainer's in-session intent act — *"I would say
approve them"* — ratifies this record, and this in-PR flip is the recording of
that act per `grove/charters/lifecycle.md`'s `gated → approved` mover rule. The
record was re-read before the flip rather than flipped on age: its Codex
mandate is still live and currently under execution as
[trellis#220](https://github.com/kodhama/trellis/issues/220). Nothing in the
decided or parked state changed; only the status field caught up with the act.

This record is also the clearest specimen of the defect it sat inside for nine
days. Its own `provenance` line says *"Maintainer merge of PR #11 preserved this
record as a draft"* — the merge happened, the record of approval did not, and
nothing existed to write it.
