---
id: kodhama-0014-retire-spore
type: decision
status: gated
depends_on: [kodhama-0010-add-spore, kodhama-0011-spore-plugin-channel]
owner: agent
updated: 2026-07-24
provenance: maintainer decision 2026-07-24 to retire Spore after reassessing its narrow macOS Terminal/Claude Remote-Control session-driver purpose; merge requested as the human-owned ship act.
---

# Decision: retire Spore as a steward and delivery channel

## Decision state

**Decided** (maintainer, 2026-07-24):

- **Spore is retired from the stewards.** It is no longer a family member or
  an active delivery surface.
- The `spore@kodhama` Claude Code marketplace entry is removed. No Codex
  package, catalog entry, or support claim will be created for the retired
  session-driver tool.
- The existing `kodhama/spore` repository and its history are retained. This
  decision does not delete source, archive the repository, or remotely
  uninstall already-installed copies.
- `kodhama-0010` and `kodhama-0011` remain as historical records with forward
  pointers here; their admission and plugin-channel decisions are superseded.
- Retirement makes no claim about the name’s future function. Any later
  product using **Spore** requires a new decision and earns its family standing
  and delivery channels from scratch.

**Open** (0):

- None.

**Parked** (1):

- **Possible future meaning:** brainstorm whether “spore” could name a
  concrete function involving dispersion, germination, or work outside the
  main forest. This is exploration, not continuity: no future concept inherits
  the retired tool’s code, membership, users, or channels by default.

## Decision

The Kodhama family retires **Spore**, the macOS Terminal.app automation and
Claude Code Remote-Control session-driver tool admitted by `kodhama-0010` and
packaged by `kodhama-0011`.

The retirement is effective at the family boundary:

1. Spore leaves the stewards enumerations in this repository.
2. `spore@kodhama` leaves the canonical Claude Code marketplace.
3. No Codex work is authorized for the retired tool.
4. Existing source and historical decisions remain readable.
5. Existing user installations are not mutated; users may uninstall them
   through their host when convenient.

Marketplace caches may continue to show the old entry until they refresh; the
retirement removes canonical discovery, not every cached copy immediately.

This is retirement, not a rename or a promise to repurpose. The name’s
dispersion/germination metaphor is worth exploring only after a real user,
problem, and operating boundary emerge.

## Why

`kodhama-0010` records the exact forcing case: hot-migrating one running Claude
Code Remote-Control session onto a Grove plugin update without losing context.
Its five Terminal-driving skills served that narrow macOS workflow and sat
outside the family’s runtime dependency chain. `kodhama-0011` then gave the
tool a family marketplace channel.

The maintainer has now judged that this narrow machinery does not justify
continued family membership and should not be carried into the native Codex
program recorded by `kodhama-0013`. Preserving it merely to defend the name
would invert the product process: a family member needs a durable problem and
function, not a metaphor searching for work.

## Consequences

### Landed with this decision

- Remove Spore from `README.md` and `CLAUDE.md`.
- Remove Spore from `.claude-plugin/marketplace.json` and its marketplace
  description.
- Add forward pointers to `kodhama-0010`, `kodhama-0011`, and the parked Spore
  note in `kodhama-0013`.

### Follow-up outside this repository

- Remove Spore from the `kodhama/kodhama` front-door enumeration.
- Update the `kodhama/stewards` GitHub description if it still lists Spore.
- Mark `kodhama/spore` as retired in its own README. Archiving the repository
  is an optional, separately authorized administrative action.

## Acceptance criteria

- **AC1:** No current stewards enumeration lists Spore.
- **AC2:** The `@kodhama` Claude marketplace contains no Spore entry and its
  description does not advertise Spore.
- **AC3:** `kodhama-0010` and `kodhama-0011` point forward to this decision;
  their historical content is otherwise unchanged.
- **AC4:** `kodhama-0013` records its parked Spore question as settled by this
  retirement without changing the Trellis/Grove/Wisp Codex mandate.
- **AC5:** No source repository, installed plugin cache, or user file is
  deleted by this change.

## Self-check (gate)

The decision supersedes the two approved Spore decisions append-only, removes
only current family/discovery surfaces owned by this repository, preserves
source history and existing installations, and makes outside-repository work
explicit rather than silently performing it. There are no open decision items.
Promote `draft → gated`; the maintainer’s requested merge is the ship act.
