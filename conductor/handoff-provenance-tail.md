# Handoff: provenance-program tail + tracked backlog

Written 2026-07-13 to brief a fresh session (a laptop conductor seat — all
family repos have local clones there). The artifact-conformance & lifecycle
program (kodhama#31) is **functionally complete**: the principle/operational
split (kodhama-0008) is ratified and rolled out family-wide, and grove's
edge-taxonomy companion (`adr-0011`, `informed_by`) is installed in all four
consumers (kodhama/wisp/design-system/trellis — the last companion install
landed as kodhama#38, 2026-07-13). What remains is one PR at the maintainer's
gate, one tier-blocked task, and a non-blocking backlog. None of it blocks
anything else.

## 1. Merge — `trellis#157` (the only open PR)

The trellis consumer provenance-edge migration — the last node of the
provenance program (`decision-0047` → trellis#155 → grove `adr-0011` → family
rollout → **this**).

- **What:** on 10 live / revise-in-place trellis artifacts (`specs/0001`,
  `specs/0002`, `research/0002·0003·0005·0006·0007·0008·0009`,
  `core/invariants/trellis-invariants-v1`), `research-*`/`brief-§*` referents
  moved out of `depends_on` into a new `informed_by` list; every coupling
  referent stayed; `decisions/` untouched (frozen append-only = exempt,
  `decision-0047` Consequence 4). No spec-0001 schema change, no `version`
  bumps (marking-class), `status` unflipped, dated amendment notes throughout.
- **Gate:** independent `conformance-reviewer` re-derived every migrated edge
  from source against `decision-0047`'s contingency test → **PASS**
  (`research-0003`/`research-0008` noted as nearest the coupling line, both
  confirmed provenance). `mergeable_state: clean`.
- **Action:** review the diff and merge. This closes the in-session slice of
  the provenance program. It is the maintainer's intent act — nothing on it
  waits on an agent.

## 2. math-quest provenance migration (needs a math-quest-sourced session)

The only remaining program task. **Cannot be done from a kodhama-tier
session** — mid-session `add_repo` for `gundisalwa/math-quest` is refused
cross-tier (verified 2026-07-12/13). Start a session **sourced from
`gundisalwa/math-quest`**.

- **What to do:** apply `decision-0047`'s discriminator to math-quest's
  **live** specs/research. Referents that merely *informed* construction
  (`research-*`, `discovery-*`, `feedback-*`, `brief-*` — ~22 discovery + 3
  feedback edges) move `depends_on` → `informed_by`; coupling referents (a
  source the artifact's correctness is/was contingent on) stay. **Frozen ADRs
  are exempt** (append-only can't be edited), so most math-quest edges won't
  move.
- **Grammar:** methodology-defined via the installed `.grove/relations.md`
  (`adr-0011`) — no schema change. Marking-class: no version bumps, status
  unflipped, dated amendment note per artifact.
- **Gate:** independent `conformance-reviewer` (the role whose duty *is*
  adjudicating coupling-vs-provenance), then the maintainer's merge.

## 3. Non-blocking backlog (kodhama#31 tail — none of it gates anything)

- **trellis#153** — record spec-0001 §2's execution-layer-approved answer
  (gate-outcome-not-status) as a small trellis decision. Smallest open
  shaping item.
- **grove#52** — `adr-0010`'s missing `changes:` field (`[consider]`, soft,
  no violation).
- **grove#55** — reference-payload charter-link 404s (bare relative links);
  charter-link normalization rides it.
- **kodhama#32** — family-conventions plugin, idea-stage.
- **grove#40 / #47** — parked `[consider]`s (grove-internal copy-sync
  mechanics; README role), now grounded.
- **grove#38** — deferred family-wide verifiable guard.
- The physical spec-reorg from `adr-0004` Consequences.

## Working conventions (for the conductor seat)

- Canonical grammar homes, all in **grove**: `charters/relations.md` (edge
  taxonomy, `adr-0011`), `charters/versioning.md` (`adr-0010`),
  `charters/lifecycle.md` (`adr-0008`) — each installed to consumers as
  `.grove/*.md`. Three-copy sync for charters
  (`charters/` ↔ `.claude/agents/` ↔ `plugins/grove/reference/agents/`).
- Each lane is its own PR in its own repo. Approval is always the maintainer's
  in-PR status flip / merge — the intent gate never opens to an agent.
- Every substantive artifact goes through an independent gate (spec-adversary
  pre-approval; conformance-reviewer at execution) before the maintainer's
  act. The builder does not grade itself.
- Family layering (kodhama-0008): trellis carries the **principles**
  (mechanism-free); grove carries the **operating model** (mechanics);
  kodhama-meta coordinates rollout and defines no mechanics.
