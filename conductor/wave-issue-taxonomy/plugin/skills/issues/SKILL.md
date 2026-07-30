---
name: issues
description: The kodhama issue convention — how to file, type, prioritise, label, and search GitHub issues in any kodhama repo. Titles are prose; every dimension lives in structured metadata.
when_to_use: Use when creating, filing, triaging, labelling, closing, or searching a GitHub issue; when writing an issue title or body; when deciding what kind of work an issue represents; or when a user asks what label, type, or priority something should get.
---

# The kodhama issue convention

**One fact, one home.** Every dimension below lives in exactly one place. If a
fact is already in the issue type, it does not also go in the title, the body,
or a label.

This describes how issues are *filed*. It applies to the issue at hand — the
one being created or edited. It is not an instruction to sweep the backlog.

## The rule that does the most work

**Issue titles are prose. No `[brackets]`, no `type:` prefixes, no `HIGH:`.**

The title says what the issue is about, in words a human reads. Everything a
machine needs to filter on is structured metadata.

```
✗  [execution] [high-priority] Fix the retry loop in the dispatcher
✓  Dispatcher retry loop drops the final attempt
   → type Bug · priority: p1 · stage: building · area: dispatcher
```

If you find yourself wanting a prefix, the dimension you're reaching for is
below. Use it instead.

## Filing an issue

Set these, in order. Stop as soon as you don't know — an unset field is
honest; a guessed one is noise.

| # | Dimension | Where it lives | Required |
|---|-----------|----------------|----------|
| 1 | **Type** | native GitHub issue type | once triaged |
| 2 | **Area** | `area: *` label | if the repo defines any |
| 3 | **Priority** | `priority: *` label | only when elevated or explicitly low |
| 4 | **Stage** | `stage: *` label | always, on open issues |
| 5 | **Status** | `blocked` · `deferred` · `needs-human` | only when true |

### 1. Type — what kind of thing is this?

Exactly one. This is a **native GitHub issue type**, not a label — set it with
`gh issue create --type` or `gh issue edit --type`.

| Type | Use when | Not this when |
|------|----------|---------------|
| `Bug` | Something behaves wrong against a stated expectation | Nothing was ever promised → `Feature` |
| `Feature` | A new capability | It's a defect against something promised → `Bug` |
| `Task` | Maintenance with an obvious done state — chores, cleanups, test gaps, rollouts, bookkeeping | The outcome is unknown → `Research` |
| `Research` | An open question to answer. The deliverable is a finding, not a change | You already know the answer and just need it built → `Task` |
| `Decision` | A choice that must be made and recorded | The choice is already made and just needs doing → `Task` |
| `Epic` | A container for sub-issues that ship separately | It ships as one unit → whatever it actually is |

**The vocabulary is closed. Never invent a type.** If nothing fits, use the
nearest match and say so in the body.

**There is no `Idea` type.** "Idea" is not a kind of thing — it's a
*commitment level*, and commitment is what stage tracks. An unvalidated
feature proposal is `Feature` at `stage: triage`. If you can't yet tell what
kind of thing it is, **leave the type unset and set `stage: triage`** —
deciding the type is what triage is for.

**Never name a type after a workflow step.** An issue that needs divergent
research is `Research` at `stage: shaping` — never a type called
`divergent-research`. The type says what the issue *is*; the stage says where
it *is*. Grove maps its steps onto stages, not the reverse.

### 2. Area — what part of the system?

`area: <thing>` labels, defined **per repo**. Deliberately not standardised
across the family: `area: dispatcher` in grove and `area: tutoring` in
math-quest have nothing to do with each other.

Use an existing one. Only propose a new area when three or more issues would
carry it.

### 3. Priority

| Label | Means |
|-------|-------|
| `priority: p0` | Drop other work. Something is broken or blocking now |
| `priority: p1` | Next up. Ahead of unlabelled work |
| *(no label)* | Normal. **This is most issues** |
| `priority: p2` | Explicitly deprioritised, but still wanted |

Do not label normal-priority work. An unlabelled issue is the default, not an
oversight.

### 4. Stage — where in the pipeline?

`stage: *` labels. Every open issue has exactly one.

`stage: triage` → `shaping` → `spec` → `ready` → `building` → `review`

- `triage` — **noticed, not yet committed to.** The type may still be unset.
  This is the collective's "we should look at this" pile
- `shaping` — accepted; the problem is being refined
- `spec` — a contract is being written
- `ready` — approved and dispatchable; an agent can pick this up
- `building` — implementation in flight
- `review` — built, awaiting verification

Closed vocabulary, one at a time. Moving an issue forward replaces the label
rather than adding to it.

**Leaving `triage` is the acceptance moment**: the type gets set and the
issue enters the pipeline. Everything in `triage` is fair game to close as
`not-planned` — that's what the pile is for.

### 5. Status — what's true right now?

Additive, and only when true. Closed vocabulary.

- `blocked` — cannot proceed. **Say what blocks it in the body, with a link**
- `deferred` — consciously parked. Not the same as low priority
- `needs-human` — requires a person; an agent must not proceed alone
- `needs: design-system` — blocked on an upstream design-system change

## Closing

Always give a reason: `gh issue close --reason completed|not-planned`.
`not-planned` covers won't-do, duplicate, and stale. Link the survivor in a
comment before closing a duplicate.

## Searching

Because the metadata is structured, search it directly:

```bash
gh issue list --type Bug --label "priority: p0"
gh issue list --label "stage: triage"                             # the untriaged pile
gh issue list --type Research --label "stage: shaping"
gh issue list --label "stage: ready" --json number,title,labels   # agent-dispatchable
gh search issues --owner kodhama --include-prs=false "type:Bug"   # across the family
```

## Legacy issues

Many existing issues still carry `[bracket]` prefixes or superseded labels.
**Do not copy them.** When you touch such an issue for another reason, filing
it correctly is welcome; converting the backlog is a separate, explicitly
approved exercise with its own mapping table.

## Full reference

`reference/taxonomy.md` — the rationale behind each dimension, the
type-versus-stage distinction, and the questions still open. Read it when a
case doesn't fit the summary above.
