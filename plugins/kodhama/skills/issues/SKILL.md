---
name: issues
description: The kodhama issue convention — titles are prose, every dimension lives in structured metadata. Use when creating, filing, triaging, labelling, closing or searching a GitHub issue; when writing an issue title or body; when starting or finishing work on one; when deciding what kind of work an issue represents; or when asked what label, type or priority something should get.
implements: kodhama-0026-issue-taxonomy
---

# The kodhama issue convention

Implements `kodhama-0026-issue-taxonomy`. That record fixes the vocabularies;
this skill states how to apply them. Where they disagree, the record wins.

**One fact, one home.** Every dimension below lives in exactly one place. If a
fact is already in the issue type, it does not also go in the title, the body,
or a label.

**Two things never become labels.** Where a request came from ("a user asked
for this", "surfaced in design review") goes in the **body**. What an issue
depends on goes in a **native dependency edge**. Neither gets a label, and
neither gets a new namespace.

**No repo hand-authors a copy of this convention** — not a README section, not
an index, not a `CONTRIBUTING` paragraph. A bare pointer to this skill is
fine; a restatement goes stale and then competes.

This describes how issues are *filed*. It applies to **the issue at hand**.
It is never an instruction to sweep the backlog.

## Before you start: is this convention in force here?

It requires six issue types. Three ship with every org; three must be created:

```bash
gh api /orgs/<org>/issue-types --jq '.[] | select(.is_enabled) | .name'
```

**Select on `is_enabled`** — a disabled type still appears in the list and
still cannot be set. **If any of the six is absent or disabled** — `Bug`,
`Feature`, `Task`, `Research`, `Decision`, `Epic` — **this convention is not
yet in force in that org.** Say so and stop.

If the command itself fails, you cannot establish whether it is in force. Say
that and stop too — do not assume either way.

## The rule that does the most work

**Issue titles are prose. No `[brackets]`, no `type:` prefixes, no `HIGH:`.**

```
✗  [execution] [high-priority] Fix the retry loop in the dispatcher
✓  Dispatcher retry loop drops the final attempt
   → type Bug · severity: broken-feature · priority: high · stage: active · facing: user
```

**Titles state the situation, not the instruction.** A `Bug` reads as the
symptom; a `Feature`, `Task` or `Epic` reads as the outcome. If you find
yourself writing an imperative verb first, rewrite it:

```
✗  Untrack the self-referencing node_modules symlink
✓  A self-referencing node_modules symlink blocks fresh clones
```

**A `Decision` states the question, a `Research` issue states the unknown** —
neither has a known outcome, which is what makes it one:

```
✗  Decide: should wisp file its own decision record
✓  Whether wisp files its own decision record
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

## Filing an issue

**Set the stage first.** Then work down. **Never stop at an unknown: leave
that field unset and continue.** An unset field is honest; a guessed one is
noise; a halted *procedure* loses the fields you did know.

| # | Dimension | Where it lives | Required |
|---|-----------|----------------|----------|
| 1 | **Stage** | `stage: *` label | on every open issue you file — one exemption, below |
| 2 | **Type** | native GitHub issue type | once out of `triage`; same exemption |
| 3 | **Facing** | `facing: *` label | on `Bug` `Feature` `Task` |
| 4 | **Severity** | `severity: *` label | on `Bug` |
| 5 | **Area** | `area: *` label | if the repo defines any |
| 6 | **Priority** | `priority: *` label | only when elevated or explicitly low |
| 7 | **Status** | `blocked` · `needs-human` · `deferred` | only when true |

### 1. Stage — how far has it got?

`stage: *` labels. Exactly one on every **open** issue you file. **One path,
every type** — there are no per-type variations.

`stage: triage` → `ready` → `active` → `review`

- `triage` — **not yet dispatchable.** Noticed and not committed to, or
  accepted and still being worked out. The type may be unset. This is the
  collective's "we should look at this" pile
- `ready` — **dispatchable.** Whatever had to be decided is decided; an agent
  or a person can pick this up
- `active` — started, not yet done
- `review` — done, not yet verified

Each value names **how far the issue has got**, not what anyone is doing right
now — so an issue nobody is touching keeps the stage it reached, and a
`deferred` issue keeps the stage it reached — `deferred` is a status carried on
top, not a stage of its own. **One kind of issue carries no stage at all**: a
machine-owned surface that is not work; see *An issue that is not work* below.

**Advance it on any issue you touch, not only ones you file.** Set `active`
when you start work, `review` when you finish. A `ready` label nobody removes
turns the dispatch queue into a list of work already done.

**Leaving `triage` is the commitment moment**: the type gets set and the issue
becomes dispatchable. `triage` holds both — things nobody has agreed to, and
things agreed but not yet worked out — so it is **not** a disposable pile, and
work in it may carry `deferred` or `priority: low` like anything else.

### 2. Type — what kind of thing is this?

Exactly one, set with `gh issue create --type` or `gh issue edit --type`.

| Type | Use when | Not this when |
|------|----------|---------------|
| `Epic` | It has children that ship separately, **and its own deliverable is that the set is coherent and complete** | It ships as one unit → the rows below |
| `Decision` | A choice must be made and recorded before work can proceed. **Threshold: until the choice is made there is nothing to build.** If the correct state is derivable from the upstream, it is not a `Decision` | The choice is already made, or the upstream settles it → `Bug` or `Task` |
| `Research` | **The deliverable is a finding**, not a change | The deliverable is a change → the rows below |
| `Bug` | Something is wrong against a stated expectation. **The expectation need not be about behaviour and the conflict need not be vertical** — an artifact contradicting its upstream, two peers contradicting each other, an artifact contradicting itself, or something stated and never implemented all qualify | Nothing was ever stated to expect → **the rows below** |
| `Feature` | A new capability | It is a defect against something promised → `Bug` |
| `Task` | A change to something that already exists — chores, cleanups, test gaps, bookkeeping, and **extending an existing capability to somewhere it was always meant to reach** | It is capability that did not exist before, anywhere → `Feature` |

**When two rows fire, the higher one wins.** The table is in precedence order:
`Epic` → `Decision` → `Research` → `Bug` → `Feature` → `Task`. `Epic` leads
only when **both** its conditions hold — a bucket of unrelated follow-ups has
children but no coherence deliverable, so classify it by what it delivers.

**`Define X` is not a type.** Ask whether the choice has been made, not
whether the deliverable is a document.

- *"Define how malformed metadata is handled"* — nothing is decided yet →
  `Decision`
- *"Write up the decision we agreed last week"* — the choice is made, only the
  record is missing → `Task` when the agreement lives only in someone's head or
  a conversation. **If it was stated somewhere durable** — a decision, a spec, a
  README — **and the record never followed, that is `Bug`**: something stated
  and never implemented, and `Bug` outranks `Task`. The test is whether an
  artifact already asserts it, not whether a person remembers agreeing

`Task` and `Research` are separated on **one axis — the deliverable.** A
verification chore whose outcome is unknown is `Research`, because what it
produces is a finding. **The test: if the issue closes on confirming "it
works", it is `Research`; if a change is already known to be needed, `Task`.**

**The vocabulary is closed. Never invent a type.** If nothing fits, use the
nearest match and say so in the body.

**A bucket with no shared deliverable is not an issue — split it.** Use `Epic`
only when the pieces ship as a coherent set. Several findings that are all the
same kind of fix are fine as one issue; nine unrelated ones are not.

**There is no `Idea` type.** "Idea" is not a kind of thing — it is a
*commitment level*, and commitment is what stage tracks. An unvalidated
feature proposal is `Feature` at `stage: triage`. If you cannot yet tell what
kind of thing it is, leave the type unset and stay at `stage: triage`.

**An issue that is not work.** A few issues are machine-owned surfaces — a
scheduled job's delivery point, an anchor another tool resolves against. They
have no lifecycle position: `triage`/`ready`/`active`/`review` all say how far
work has got, and these never get anywhere by design. **Leave both the type and
the stage unset, and say so in the body.** This is the only exemption from
dimensions 1 and 2 of the table above — and it is not a per-type variation,
because these are not work of any type.

**Do not close it** — something may be resolving against it, and closing it
breaks that thing. If such an issue carries a label a tool matches on, that
label is a mechanical anchor, not a taxonomy dimension: leave it alone.

**Never name a type after a workflow step.** An issue needing divergent
research is `Research`, never a type called `divergent-research`. The type
says what the issue *is*; the stage says where it *is*.

### Hierarchy — native sub-issues

```bash
gh issue create --title "..." --parent 42     # file under an epic
gh issue edit 57 --add-sub-issue 61           # attach an existing issue
gh issue view 42 --json subIssues             # read the children
```

**An `Epic`'s stage is its own and is never computed from its children** — at
any stage. An epic whose own coordination is finished is at `review` even with
children still open, and an epic at any stage may hold children at any mix.

### 3. Facing — who observes the difference?

`facing: user` · `facing: system`. Required on `Bug`, `Feature` and `Task`.

**The boundary is this repository's output**, not who maintains what:

| | |
|---|---|
| `facing: user` | it changes what someone **consuming this repo** gets — a product's users, or another repository that installs or depends on it |
| `facing: system` | it changes only how this repo is built or maintained |

Who maintains the consumer is irrelevant. A change a sibling repo would notice
is `facing: user` even when the same people maintain both.

**An artifact-only change is `facing: system`** even when the artifact governs
shipped output — a wrong spec is why the plugin will be wrong, but the
consumer receives the plugin, not the spec. It becomes `facing: user` only
when what consumers receive changes.

**`Decision`, `Research` and `Epic` carry no `facing:`.** A record, a finding
and a coherence guarantee are none of them a change a consumer receives.

**This is where Story and Enabler live.** A `Feature` at `facing: user` is
what agile calls a **Story**; at `facing: system`, an **Enabler**.

### 4. Severity — how bad is it for whoever hits it?

`severity: *` labels, required on `Bug`. **Severity is impact; priority is
urgency.** They are different axes and a bug can be high on one and low on the
other.

| Label | Means |
|-------|-------|
| `severity: blocker` | someone is stopped, with no way through |
| `severity: broken-feature` | a path is unusable or misleading; the default path still works |
| `severity: papercut` | annoying, cosmetic, or has a workaround |

**When two fire, take the more severe.** They overlap by construction — a
blocker also makes a path unusable.

**For a bug in an artifact rather than in running behaviour** — a spec
contradicting its upstream, two documents disagreeing, something stated and
never built — nothing is executing, so read it by what a reader would do:
**`broken-feature` if someone could act wrongly on it, `papercut` otherwise.**
`blocker` is for when work genuinely cannot proceed.

A papercut on the first screen every user sees can be `priority: urgent`. A
blocker in a feature nobody has enabled yet can be unprioritised. Do not
collapse the two axes.

Optional on other types when something is degraded rather than absent.

### 5. Area — what part of the system?

`area: <thing>` labels, defined **per repo**. Deliberately not standardised
across the family. Use an existing one; only propose a new area when three or
more issues would carry it.

### 6. Priority — how soon?

| Label | Means |
|-------|-------|
| `priority: urgent` | drop other work |
| `priority: high` | next up, ahead of unlabelled work |
| *(no label)* | normal. **This is most issues** |
| `priority: low` | wanted, ranked below normal |

Words rather than `p0`/`p1`/`p2` deliberately: a numbered scale reads as
monotone, and "unlabelled sits between p1 and p2" is a trap.

### 7. Status — what is true right now?

Additive, and only when true. Closed vocabulary, three bare tokens.

- `blocked` — cannot proceed, and **the blocker is not another issue**. Name
  it in the body
- `needs-human` — requires a person; an agent must not proceed alone
- `deferred` — nothing is stopping it; **we have chosen not to schedule it
  yet**, until a condition named in the body

**Use the most specific one, and never add `blocked` on top of it.**
`needs-human` is a specific form of blocked; `blocked` is the general form for
everything else. They do not combine.

**`blocked` and `deferred` are not the same shape.** `blocked` means the work
*cannot* proceed; `deferred` means it *could* but we decided not to.

**Any status label suspends dispatch.** `stage: ready` means the work is
dispatchable in principle; a status label withholds it. The issue **keeps its
stage** — the status is what withholds it.

### Blocked by another issue — use the native dependency

```bash
gh issue create --title "..." --blocked-by 42
gh issue edit 57 --add-blocked-by 42      # --remove-blocked-by to clear
gh issue list --json number,title,blockedBy
```

This covers cross-repo blockers too, including waiting on a design-system
change. The `blocked` label is only for blockers that are **not** issues.

### "Not now" — three states, one question each

| | Has it been committed to? | Consequence |
|---|---|---|
| `stage: triage` | **Not necessarily** — it holds both | any priority, and `deferred` if a condition is named. The stage does not decide this; the body does |
| `priority: low` | Yes, ranked low | competes for time, just badly |
| `deferred` | Yes, but waiting on a **stated condition** | does not compete until the condition holds |

If you cannot name the condition, it is not `deferred` — it is
`priority: low`.

## Closing

Always give a reason. **The token has a space and needs quoting** — `gh`
accepts exactly `completed`, `"not planned"`, and `duplicate`:

```bash
gh issue close 57 --reason completed
gh issue close 57 --reason "not planned"     # won't-do, stale
gh issue close 57 --duplicate-of 42          # native edge; implies --reason duplicate
```

**Use `--duplicate-of`, not a comment** — it records the survivor as a real
edge, the same reason blocking uses `--blocked-by` rather than prose.

## Searching

```bash
gh issue list --type Bug --label "severity: blocker"
gh issue list --label "stage: triage"                             # the untriaged pile
gh issue list --label "stage: ready" --json number,title,labels \
  --search '-label:needs-human -label:blocked -label:deferred'    # agent-dispatchable
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
questions still open.
