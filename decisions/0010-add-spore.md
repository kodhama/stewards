---
id: kodhama-0010-add-spore
type: decision
status: superseded  # retired by kodhama-0014 (2026-07-24); original ratification: PR #7 merge (2026-07-22)
depends_on: [kodhama-0001-family-delivery, kodhama-0002-delivery-channels, kodhama/kodhama-0009-org-topology-spirit-stewards-trees]
superseded_by: [kodhama-0014-retire-spore]
owner: agent
updated: 2026-07-22
provenance: maintainer request 2026-07-22 to formally admit spore (Claude Code session-driver skills, github.com/kodhama/spore) to the stewards after its first public commit. spore was distilled 2026-07-22 from a live session that used it to hot-migrate a running session onto the grove thin-vendor plugin.
---

# Decision: spore joins the stewards — the session-driver tool

> **Superseded by `kodhama-0014-retire-spore` (2026-07-24).** Spore is no
> longer a steward. This file remains the historical record of its admission.

**Decision.** **spore** (`github.com/kodhama/spore`) is admitted to the
**stewards** as a full family member, listed as **spore (session drivers)**.
It is a *steward*, not a *tree* (`kodhama-0009`): scaffolding that tends the
maintainer's work on the forest, not a product cultivated by it.

## What spore is

macOS Terminal.app automation — a handful of Claude Code skills that spawn,
hot-fork, and tend Remote-Control sessions and plugins *from the side*:
`fork-here` (resume the running session onto a plugin update without losing
context — the headliner), `side-session`, `pull-plugin`, `peek-session`,
`close-session`. No binary, no service; installed user-scope via `install.sh`.

## Why it is a steward

- It **tends the collective's own tooling loop**, not any product. The forcing
  case that produced it (2026-07-22): the grove thin-vendor migration moved the
  chartered agents into a plugin, and a *running* session could not adopt them
  without a restart — which loses context, and `/plugin` is unavailable over
  Remote Control. spore closes exactly that gap. That is steward work.
- It sits **outside the runtime dependency chain** (`wisp → grove → trellis`):
  it depends on none of the triad and nothing depends on it at runtime. A
  peripheral operator tool, admitted for family coherence (one home, one
  install story, the shared governance overlays), not because anything consumes
  it.

## Placement and delivery

- **Ordering.** Appended last in every enumeration —
  `trellis · grove · wisp · design-system · homebrew-tap · spore` — the newest
  member and outside the built→living→spirit triad, so it does not disturb the
  established causal order (`kodhama-0003`).
- **Delivery channel** (`kodhama-0001`/`0002`): own repo, own README, MIT,
  self-applies the grove + trellis overlays like the other tool members. It is
  **not** a Claude Code plugin today, so it does **not** join the `@kodhama`
  marketplace manifest (`.claude-plugin/marketplace.json`) — same as wisp,
  design-system, and homebrew-tap. If it is ever packaged as a plugin, a
  marketplace entry is the follow-up, not this decision.

## Scope of this change (the enumeration edits this decision ratifies)

1. `stewards/README.md` — append `· [spore](…) (session drivers)`.
2. `stewards/CLAUDE.md` — same, in the member sentence.
3. `kodhama/README.md` — same, in the stewards enumeration (org front door).
4. GitHub repo description of `kodhama/stewards` — append `· spore` to the
   parenthetical member list.

No plugin/marketplace change; no dependency-direction change (spore is outside
the chain).

## Self-check (gate)

Load-bearing facts verified this session: the family enumerations were read
from the live `main` of each repo before editing; spore's repo exists and is
public (`github.com/kodhama/spore`, first commit pushed 2026-07-22); spore
ships no plugin manifest, so its marketplace absence matches wisp/DS/tap, which
were confirmed absent from `marketplace.json`. Ordering appends last, leaving
the triad order intact. `draft → gated → approved`, ratified by the maintainer's merge of PR #7.
