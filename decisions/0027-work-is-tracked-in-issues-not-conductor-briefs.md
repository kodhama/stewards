---
id: kodhama-0027
type: decision
status: approved  # maintainer intent act 2026-08-02, in session: "I would say approve them" — an in-PR flip recording that act, per grove/charters/lifecycle.md's gated -> approved mover rule; the merge performs the ship. Raised by the maintainer 2026-08-01 after a ledger reconciliation: "I question whether this ledger approach warrants a file or an issue... we're leaning more towards having these things in issues."
depends_on: [kodhama-0026-issue-taxonomy, kodhama-0009-org-topology-spirit-stewards-trees]
owner: agent
date: 2026-08-01
---

# 0027 — work is tracked in issues; the conductor brief stops being a ledger

## Context

`CLAUDE.md` mandates the practice: *"each cross-repo wave gets a brief in
`conductor/`; **the brief IS the ledger** — check items off in the same commits
that report them."*

**It does not hold, and the failure is structural rather than a lapse.**
Measured 2026-08-01:

- **14 conductor briefs exist; 12 have not been touched in one to three-plus
  weeks.** Briefs go quiet and stay quiet. That is the norm, not the exception.
- **`wave-family-consolidation.md` has now been reconciled twice, with the same
  diagnosis both times.** 2026-07-29, in the file: *"twelve entries were stale in
  both directions — items marked open that had landed, and items marked done that
  were only triaged … **fourteen items of the wave's actual plan appear nowhere in
  this brief at all**. Judged by this brief the wave looked nearly finished. It is
  not."* Then 2026-08-01: three days and roughly ten merged PRs with no update.

**The mechanism is duplication.** An issue's state updates as a *side effect of
doing the work* — close it and the state is correct. A ledger's state updates only
if someone remembers to write it down, and the remembering competes with the work
it describes. Every work item in a brief already exists as an issue or a merged
PR, so the brief is a second copy that can only ever drift.

That also puts the practice in tension with this repo's own rule: **one home per
kind of information**.

**Why it was reasonable, and what changed.** The practice dates from a period when
work was tracked in the repository — roadmap files in-tree, `math-quest` still
carries one — and GitHub was mainly somewhere to launch workers from a laptop.
Those workers hit max-turn limits constantly. Since `/rc` and cloud sessions the
launcher role has gone, and what remains of GitHub is the part that was always
better: **issues with state, types and native dependency edges.**
`kodhama-0026`'s taxonomy made that half usable; this record retires the half it
replaced.

## Decision

**1. Work is tracked in GitHub issues.** Every item a wave would have listed — a
task, a bug, a parked question, a follow-up — is an issue in the repository that
owns the work, typed and labelled per `kodhama-0026`. A wave with cross-repo scope
uses an `Epic` and native dependency edges, not a file that names issues living
elsewhere.

**2. The conductor brief stops being a ledger.** `CLAUDE.md`'s clause is amended:
no checkbox lists, no per-item status, no "open/closed" columns duplicating issue
state. **A brief that lists work is a brief that will be wrong.**

**3. What a brief may still hold is narrative that has no issue shape** — the
reasoning behind a sequence, a trace that justified a removal, a closure report.
Recorded because deleting the form outright would lose the one thing it does that
issues do not.

**4. Lessons and traps do NOT go in a per-wave brief either.** Their value is
cross-wave and retrospective — *"a matcher pair drifted four times before one
normalisation replaced two hand-matched regexes"* is useful to the next wave, not
this one. Burying it in a file that dies with its wave is why the same traps keep
being rediscovered. They belong in one durable, searchable home; **which home is
Open question 1**, deliberately unresolved here rather than guessed.

**5. Existing briefs become archive, not debt.** They are not migrated or
deleted. They stop being updated, and nothing should be read from them as current
state. `wave-family-consolidation.md`'s 2026-08-01 reconciliation is the last one
it gets.

## Consequences

- `CLAUDE.md`'s conductor clause is rewritten in the same change that ratifies
  this.
- `stewards#71` — a PR reconciling the ledger, opened hours before this record —
  is superseded by it. Merging it would invest further in the format being
  retired; it is closed with a pointer here.
- The parked-questions rule (*"batch to the human ≤3 at a time"*) survives
  unchanged. It is about how questions reach a human, not about where work lives.

## Open questions

1. **Where do cross-wave lessons and traps live?** Not a per-wave brief (D4), and
   they are poorly shaped as issues — they are not work, they are things learned.
   Candidates: one living document in `conductor/`; issues typed `Research`; or
   the agent's own memory, which is where several of these already are and which
   no human can read. Unresolved.
2. **Does `math-quest`'s roadmap file fall under this?** It is the same shape from
   the same era, in a product repo rather than here. This record does not reach
   it; naming it so the inconsistency is deliberate rather than overlooked.
