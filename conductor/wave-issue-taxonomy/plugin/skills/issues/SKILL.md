---
name: issues
description: The kodhama issue convention — how to file, type, prioritise, label, and search GitHub issues in any kodhama repo. Titles are prose; every dimension lives in structured metadata.
when_to_use: Use when creating, filing, triaging, labelling, closing, or searching a GitHub issue; when writing an issue title or body; when deciding what kind of work an issue represents; or when a user asks what label, type, or priority something should get.
---

# The kodhama issue convention

**One fact, one home.** Every dimension below lives in exactly one place. If a
fact is already in the issue type, it does not also go in the title, the body,
or a label.

This describes how issues are *filed*. It applies to **the issue at hand** —
the one you are creating or editing. It is never an instruction to sweep the
backlog.

## Before you start: is this convention in force here?

It requires six issue types. Three ship with every org; three must be created:

```bash
gh api /orgs/<org>/issue-types --jq '.[].name'
```

**If any of `Research`, `Decision` or `Epic` is absent, this convention is not
yet in force in that org.** Say so and stop — do not file half-typed issues
against it. Provisioning is a setup step, not a case to work around.

If the command itself fails (no `read:org`, network, unknown org), you cannot
establish whether it is in force. Say that and stop too — do not assume
either way.

## The rule that does the most work

**Issue titles are prose. No `[brackets]`, no `type:` prefixes, no `HIGH:`.**

The title says what the issue is about, in words a human reads. Everything a
machine needs to filter on is structured metadata.

```
✗  [execution] [high-priority] Fix the retry loop in the dispatcher
✓  Dispatcher retry loop drops the final attempt
   → type Bug · priority: p1 · stage: active · facing: user
```

**Titles state the situation, not the instruction.** "Fix X" and "Add Y" name
the response; the title names what is true. A `Bug` reads as the symptom;
everything else reads as the outcome. If you find yourself writing an
imperative verb first, rewrite it:

```
✗  Untrack the self-referencing node_modules symlink
✓  A self-referencing node_modules symlink blocks fresh clones
```

**A `Decision` states the question, a `Research` issue states the unknown** —
neither has a known outcome, which is what makes it one:

```
✗  Decide: should wisp file its own decision record
✓  Whether wisp files its own decision record
✗  Run a controlled experiment on reviewer value
✓  Whether a second automated reviewer earns its subscription
```

**Where the issue has a consumer, state the outcome from their side.**

```
✗  Add streak-freeze logic to the progress reducer
✓  A learner's streak survives one missed day
```

**Never invent a consumer that does not exist.** Some work changes nothing
anyone consuming this repo would get — a refactor, a lint rule, a test gap.
That is fine and needs no persona:

```
✗  As a maintainer, I want the reducer to be easier to reason about
✓  Progress reducer duplicates streak logic across three branches
```

The test is whether you can name a real party who would notice. If you cannot,
the issue is `facing: system` and the plain outcome is the honest title.

## Filing an issue

**Set the stage first.** Then work down. **Never stop at an unknown: leave
that field unset and continue.** An unset field is honest; a guessed one is
noise; a halted *procedure* loses the fields you did know.

| # | Dimension | Where it lives | Required |
|---|-----------|----------------|----------|
| 1 | **Stage** | `stage: *` label | on every open issue **you file** |
| 2 | **Type** | native GitHub issue type | once out of `triage` |
| 3 | **Facing** | `facing: *` label | on `Bug` `Feature` `Task` `Epic` |
| 4 | **Area** | `area: *` label | if the repo defines any |
| 5 | **Priority** | `priority: *` label | only when elevated or explicitly low |
| 6 | **Status** | `blocked` · `needs-human` · `needs-design-system` · `deferred` | only when true |

### 1. Stage — where in the pipeline?

`stage: *` labels. Exactly one on every **open** issue you file. On an issue
you are only editing for some other reason, adding one is permitted, not
required — the same rule as Legacy below.

`stage: triage` → `shaping` → `drafting` → `ready` → `active` → `review`

- `triage` — **noticed, not yet committed to.** The type may still be unset.
  This is the collective's "we should look at this" pile
- `shaping` — accepted; the problem is being refined
- `drafting` — the artifact that defines the work is being written
- `ready` — approved and dispatchable; an agent can pick this up
- `active` — the committed work is in flight
- `review` — done, awaiting verification

**Not every type visits every stage.** Take the path for your type:

| Type | Path |
|---|---|
| `Bug` `Feature` `Task` `Epic` | the full path above |
| `Decision` | `triage` → `shaping` → `ready` → `drafting` → `review` |
| `Research` | `triage` → `shaping` → `ready` → `active` → `review` |

`Decision` has no `active`: writing the record *is* its work, so `drafting`
is the working stage and `ready` precedes it — a shaped decision awaiting an
author is exactly "dispatchable". `Research` has no `drafting`: the work *is*
the finding. In every path `ready` sits immediately before the stage where
the work happens. Skipping a stage your type does not have is correct, not an
omission.

**Stage marks how far the issue has got, not what is happening this minute.**
An issue at `stage: shaping` that nobody is touching is still at `shaping`.
That is why a `deferred` issue keeps the stage it reached rather than needing
one of its own.

**On close, strip the stage label.** A closed issue carrying `stage: active`
asserts something false. **On reopen, set the stage the work is actually at**
— `triage` only if it genuinely needs re-deciding.

### 2. Type — what kind of thing is this?

Exactly one. This is a **native GitHub issue type**, not a label — set it with
`gh issue create --type` or `gh issue edit --type`.

| Type | Use when | Not this when |
|------|----------|---------------|
| `Epic` | It has children that ship separately, **and its own deliverable is that the set is coherent and complete** | It ships as one unit → the rows below |
| `Decision` | A choice must be made and recorded before work can proceed. **Threshold: until the choice is made there is nothing to build.** If the correct state is derivable from the upstream, it is not a `Decision` | The choice is already made, or the upstream already settles it → `Bug` or `Task` |
| `Research` | **The deliverable is a finding**, not a change | The deliverable is a change → the rows below |
| `Bug` | Something is wrong against a stated expectation — **including an artifact contradicting an approved upstream, where nothing "behaves" at all** | Nothing was ever promised → `Feature` |
| `Feature` | A new capability | It is a defect against something promised → `Bug` |
| `Task` | The deliverable is a change to something that already exists — chores, cleanups, test gaps, bookkeeping, and **extending an existing capability to somewhere it was always meant to reach** | It is capability that did not exist before, anywhere → `Feature` |

**When two rows fire, the higher one wins.** The table is in precedence order:
`Epic` → `Decision` → `Research` → `Bug` → `Feature` → `Task`. `Epic` leads
only when **both** its conditions hold — children that ship separately *and*
coherence-of-the-set as its own deliverable. A bucket of unrelated follow-ups
has children but no such deliverable, so it is not an `Epic`; classify it by
what it actually delivers.

An issue that both reports a contradiction *and* requires choosing how to
resolve it is a `Decision`. An issue that is both a rollout and an open
question is `Research`.

`Task` and `Research` are separated on **one axis only — the deliverable.** A
verification chore whose outcome is unknown is `Research`, because what it
produces is a finding.

**The vocabulary is closed. Never invent a type.** If nothing fits, use the
nearest match and say so in the body.

**There is no `Idea` type.** "Idea" is not a kind of thing — it is a
*commitment level*, and commitment is what stage tracks. An unvalidated
feature proposal is `Feature` at `stage: triage`. If you cannot yet tell what
kind of thing it is, leave the type unset and stay at `stage: triage` —
deciding the type is what triage is for.

**Never name a type after a workflow step.** An issue needing divergent
research is `Research` at `stage: shaping` — never a type called
`divergent-research`. The type says what the issue *is*; the stage says where
it *is*.

### Hierarchy — native sub-issues

```bash
gh issue create --title "..." --parent 42     # file under an epic
gh issue edit 57 --add-sub-issue 61           # attach an existing issue
gh issue view 42 --json subIssues             # read the children
```

An `Epic`'s stage is **its own**, describing the epic's work, never computed
from its children:

- `drafting` — the epic's own breakdown work. An epic with no children yet is
  normally here
- `ready` — the breakdown is approved and the epic can be picked up
- `active` — the epic's own coordination work is in flight
- `review` — the epic's own completeness check: did the set come out coherent

**Read every one of those as describing the epic's work, not its children's
state.** An `Epic` at any stage may hold children at any mix of stages, and an
epic whose coordination is finished is at `review` even if children are still
open.

### 3. Facing — who observes the difference?

`facing: user` · `facing: system`. Set it on the delivery types — `Bug`,
`Feature`, `Task`, `Epic`. A `Decision` and a `Research` issue produce a
record and a finding, not a change anyone consumes, so they carry no
`facing:`.

**The boundary is this repository's output**, not who maintains what:

| | |
|---|---|
| `facing: user` | it changes what someone **consuming this repo** gets — a product's users, or another repository that installs or depends on it |
| `facing: system` | it changes only how this repo is built or maintained |

Who maintains the consumer is irrelevant. A change a sibling repo would notice
is `facing: user` even when the same people maintain both, and even when
nobody outside the org ever sees it.

The distinction cuts *inside* a type, not between types. Two real chores from
the same repo:

```
facing: system   Progress reducer duplicates streak logic across three branches
facing: user     Theme glyph renders flush against the name
```

Same type, entirely different audience — and the second is a learner looking
at a wrong-looking screen.

**This is where Story and Enabler live.** A `Feature` at `facing: user` is
what agile calls a **Story**; at `facing: system`, an **Enabler**. One type
seen from two sides, which is why an enabler never needs a fabricated persona
to justify itself. It has an honest home.

### 4. Area — what part of the system?

`area: <thing>` labels, defined **per repo**. Deliberately not standardised
across the family. Use an existing one; only propose a new area when three or
more issues would carry it.

### 5. Priority

| Label | Means |
|-------|-------|
| `priority: p0` | Drop other work. Something is broken or blocking now |
| `priority: p1` | Next up. Ahead of unlabelled work |
| *(no label)* | Normal. **This is most issues** |
| `priority: p2` | Accepted and wanted, ranked below normal |

Do not label normal-priority work. An unlabelled issue is the default, not an
oversight.

### 6. Status — what is true right now?

Additive, and only when true. Closed vocabulary, four bare tokens.

- `blocked` — cannot proceed, and **the blocker is not another issue**. Name
  it in the body
- `needs-human` — requires a person; an agent must not proceed alone
- `needs-design-system` — waiting on an upstream design-system change
- `deferred` — nothing is stopping it; **we have chosen not to schedule it
  yet**, until a condition named in the body

**`blocked` and `deferred` are not the same shape.** `blocked` means the work
*cannot* proceed; `deferred` means it *could* but we decided not to. "Waiting
for the vendor to ship 2.0" is `blocked`. "Not before the Q3 release" is
`deferred`.

**Use the most specific one, and never add `blocked` on top.** `needs-human`
and `needs-design-system` are specific forms of blocked. They do not combine.

### Blocked by another issue — use the native dependency

```bash
gh issue create --title "..." --blocked-by 42
gh issue edit 57 --add-blocked-by 42      # --remove-blocked-by to clear
gh issue list --json number,title,blockedBy
```

The `blocked` label is only for blockers that are **not** issues.

### "Not now" — three states, one question each

| | Has it been accepted? | Consequence |
|---|---|---|
| `stage: triage` | **No** — nobody has committed to it | no `priority: p2`, no `deferred`. `p0`/`p1` are fine — an incident is often noticed before anyone triages it |
| `priority: p2` | Yes, ranked low | competes for time, just badly |
| `deferred` | Yes, but we chose not to schedule it | does not compete until the condition holds |

If you cannot name the condition, it is not `deferred` — it is `priority: p2`.
If nobody has agreed to do it at all, it is neither; it is `stage: triage`.

## Closing

Always give a reason. **The token has a space and needs quoting** — `gh` accepts
exactly `completed`, `"not planned"`, and `duplicate`:

```bash
gh issue close 57 --reason completed
gh issue close 57 --reason "not planned"     # won't-do, stale
gh issue close 57 --reason duplicate         # native — do not fold into "not planned"
```

`duplicate` is a real close reason; use it and link the survivor in a comment.
Strip the `stage:` label on close.

## Searching

```bash
gh issue list --type Bug --label "priority: p0"
gh issue list --label "stage: triage"                             # the untriaged pile
gh issue list --label "stage: ready" --json number,title,labels \
  --search '-label:needs-human -label:blocked -label:deferred'      # agent-dispatchable
gh issue list --type Feature --label "facing: user"               # user-visible capability
gh search issues --owner <org> "type:Bug"                          # across the family
```

## Legacy issues

Many existing issues still carry `[bracket]` prefixes or superseded labels.
**Never copy them onto a new issue.** On an issue you are already editing for
another reason, normalising it is **permitted, not required**. Converting the
backlog wholesale is a separate exercise under its own approval.

## Full reference

`reference/taxonomy.md` — the rationale behind each dimension and the
questions still open. Read it when a case does not fit the summary above.
