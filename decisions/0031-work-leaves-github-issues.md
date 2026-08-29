---
id: kodhama-0031-work-leaves-github-issues
type: decision
status: approved  # maintainer intent act 2026-08-29, in session: "I also want to retire the issues skill … I will likely not use gh issues for anything else" — an in-PR flip recording that act, per .grove/lifecycle.md's gated -> approved mover rule; the merge performs the ship. The agent did not open the gate
depends_on: [kodhama-0026-issue-taxonomy, kodhama-0027, kodhama-0030-install-door-serves-trellis-only]
owner: agent
updated: 2026-08-29
provenance: "maintainer direction, 2026-08-29, given while retiring the kodhama plugin: the issue convention is to be retired, work is moving to Linear, and which remaining backlogs get ported is explicitly left open. The taxonomy's retirement — rather than its survival as a tool-independent vocabulary — was the maintainer's choice between those two options, put to them directly."
---

# 0031 — work leaves GitHub issues; the taxonomy retires with it

## Decision

**1. GitHub issues are no longer where work is tracked.** `kodhama-0027` D1
required every work item to be an issue in the repository that owns it, typed
and labelled per `kodhama-0026`. That requirement is retired. Work moves to
Linear.

**2. `kodhama-0026` is retired in full.** Its vocabularies — prose titles, the
six native issue types, and the `stage:`/`severity:`/`priority:`/`facing:`/
status/`area:` label set — were a GitHub encoding. Linear carries those
dimensions natively, so the encoding does not survive the move. It is
annotated by forward pointer in `kodhama/kodhama`, never edited.

**3. `kodhama-0027` D2–D5 survive untouched.** The conductor brief still stops
being a ledger; briefs are still archive; a brief may still hold narrative that
has no issue shape; lessons and traps still do not go in one. **That reasoning
was never about GitHub.** D1's diagnosis — *"a ledger's state updates only if
someone remembers to write it down"* — indicts duplication, not a tracker, and
holds identically against Linear. Only D1's *destination* is superseded.

The parked-questions rule survives for the same reason: it governs how
questions reach a human, not where work lives.

**4. Porting is per-repo, unscheduled, and not owed.** No repository is
required to migrate its open issues. Two have already moved and the rest are
open questions the maintainer holds; **no issue, epic or tracking artifact is
filed for the remainder.** A repository that never ports has not failed
anything.

**5. Nothing is swept.** The seeded types and labels stay in every repository
that has them, and closed issues keep their metadata. Removing them would be
churn against a surface being abandoned.

## Why

The maintainer's direction is the reason. Two things are worth recording beside
it.

**The convention had already lost its carrier.** `kodhama-0030` D3 deleted
`plugins/kodhama/skills/issues/` — the skill that taught the taxonomy and the
actuator that seeded it — and recorded the consequence honestly in its §Cost 4:
*"The **convention** is unaffected — it lives in the decisions. Its **tooling**
is gone."* That was true when written and is the state this record ends. A
convention with no tooling, no skill and a maintainer who has stopped using its
surface is a rule that only exists to be restated.

**Adoption had already begun reversing.** Measured 2026-08-29:

| repo | open issues |
|---|---:|
| grove | 55 |
| stewards | 13 |
| sdd-gauntlet | 10 |
| wisp | 6 |
| trellis | **0** |
| math-quest | **0** |
| design-system, homebrew-tap | 0 (never had a backlog) |

`math-quest` is fully moved to Linear and `trellis` is partway, per the
maintainer 2026-08-29. On 2026-08-01 `kodhama/stewards#79` recorded trellis at
24 open and unmigrated; it is now empty. **The direction of travel is already
off GitHub**, and 0026 was being enforced against repositories leaving.

## Cost, stated

**1. 84 open issues lose their stated home without gaining one.** grove 55,
stewards 13, sdd-gauntlet 10, wisp 6. They keep working as GitHub issues — this
record does not close or migrate them — but no artifact now says where a
*new* item goes for those four repositories, and D4 deliberately declines to
schedule the port. **The gap is real and chosen**, not overlooked.

**2. Cross-repo dependency edges do not survive a partial move.**
`kodhama-0027` D1's Epic-plus-native-sub-issue shape is what
`kodhama-0029` D5 relies on for tracking a decision's downstream work. With
some repositories on Linear and some on GitHub, a cross-repo epic can no longer
span them natively. `kodhama-0029` D5 is not superseded here — it names a
mechanism that now works only within one tracker, and this record does not
pretend otherwise.

**3. `kodhama-0029` D3 loses more ground.** Its rule — *anything carrying a
collective decision's effect names the deciding record by id* — cited
`plugins/kodhama/skills/issues/SKILL.md` as an exemplar. `kodhama-0030` §Cost 4
recorded that deletion leaving the argument resting on two `.grove/` files.
Retiring the taxonomy removes the `implements:`-carrying issue metadata too.
The rule stands; its evidence base keeps shrinking.

**4. The vocabulary work is discarded, not banked.** `kodhama-0026` settled two
questions against the corpus — that there is no `Idea` type, and that
commitment is a stage rather than a kind — with a discriminating test:
*"a category which dissolves the moment work finishes is a lifecycle position,
not a kind."* That reasoning is tool-independent and would have transferred.
Option 2 in the sitting that produced this record was to keep it as a portable
vocabulary; the maintainer chose the clean cut. Recorded so the choice is
visible as a choice.

## What was considered and not done

**Keeping the taxonomy as a tool-independent vocabulary**, with only its GitHub
projection retired — the abstract/concrete split `kodhama/stewards#65`
described before it was closed. Put to the maintainer directly and declined in
favour of retiring it with the surface.

**Filing a port-the-backlog issue per repository.** Rejected on the maintainer's
words: *"I want zero follow ups."* It would also be an artifact tracked in the
system being retired.

**Sweeping the seeded labels and types from six repositories.** Rejected as
churn — see D5.

## Consequences

`kodhama-0027` keeps `status: approved` with D1 superseded here and D2–D5 live;
annotated in place by forward pointer, per `kodhama-0004` and this repository's
rule that a ratified decision is never edited.

`kodhama-0026` keeps `status: approved`, retired in full, annotated the same way
in `kodhama/kodhama`.

`CLAUDE.md`'s **Work is tracked in GitHub issues** rule is rewritten in the same
change that ratifies this. The conductor-brief half of that clause is
`kodhama-0027` D2–D5 and survives.

The twelve issues closed in this repository on 2026-08-29 under `kodhama-0030`
are unaffected; they were closed as moot, not as part of this move.
