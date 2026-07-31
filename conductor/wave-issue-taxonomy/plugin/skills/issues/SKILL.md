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

## The rule that does the most work

**Issue titles are prose. No `[brackets]`, no `type:` prefixes, no `HIGH:`.**

The title says what the issue is about, in words a human reads. Everything a
machine needs to filter on is structured metadata.

```
✗  [execution] [high-priority] Fix the retry loop in the dispatcher
✓  Dispatcher retry loop drops the final attempt
   → type Bug · priority: p1 · stage: active · area: dispatcher
```

**Titles state the situation, not the instruction.** "Fix X" and "Add Y" name
the response; the title names what is true. A `Bug` reads as the symptom
(*"…drops the final attempt"*); everything else reads as the outcome
(*"Dispatcher retries are configurable per route"*, *"Whether runs commit
their cursor"*). If you find yourself writing an imperative verb first, the
dimension you are reaching for is below — use it instead.

## Filing an issue

**Set the stage first — the one field every issue you touch carries.**
Then work down. **Never stop at an unknown: leave that field unset and
continue.** An unset field is honest; a guessed one is noise; a halted
*procedure* loses the fields you did know.

| # | Dimension | Where it lives | Required |
|---|-----------|----------------|----------|
| 1 | **Stage** | `stage: *` label | always |
| 2 | **Type** | native GitHub issue type | once out of `triage` |
| 3 | **Area** | `area: *` label | if the repo defines any |
| 4 | **Priority** | `priority: *` label | only when elevated or explicitly low |
| 5 | **Status** | `blocked` · `needs-human` · `needs-design-system` · `deferred` | only when true |

### 1. Stage — where in the pipeline?

`stage: *` labels. Exactly one on any issue you file or touch. That is an
invariant about **your** issue, not a claim about every issue in the repo.

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
| `Bug` `Feature` `Task` `Epic` | `triage` → `shaping` → `drafting` → `ready` → `active` → `review` |
| `Decision` | `triage` → `shaping` → `drafting` → `review` |
| `Research` | `triage` → `shaping` → `active` → `review` |

A `Decision` is never *built*, so it has no `ready`/`active`: its artifact is
the record, drafted then reviewed. A `Research` issue has no `drafting` — the
work *is* the finding. Skipping a stage your type does not have is correct,
not an omission.

**An `Epic` takes the full path**, because it is real work with its own
deliverable. Its `drafting` is the **breakdown into children**, and that
breakdown is a dispatchable artifact: an `Epic` at `ready` is one an agent can
pick up and decompose. `active` is its children in flight; `review` asks
whether the set turned out coherent and complete.

**An `Epic`'s stage is its own, never derived from its children.** It says
where *the epic* is, not where its contents are. An `Epic` at `active` may
hold children at `triage` and `review` simultaneously; that is normal, not a
contradiction. An epic nobody has agreed to sits at `triage`, and an epic with
no children yet is at whatever stage its own work has reached — often
`drafting`, since deciding what it contains is the work.

Closed vocabulary, one at a time. Moving forward replaces the label rather
than adding to it.

**Leaving `triage` is the acceptance moment**: the type gets set and the issue
enters the pipeline. Everything in `triage` is fair game to close as
`not-planned` — that is what the pile is for.

**On close, strip the stage label.** A closed issue carrying `stage: active`
asserts something false. **On reopen, set `stage: triage`** and re-decide —
the state that produced the old label no longer holds.

### 2. Type — what kind of thing is this?

Exactly one. This is a **native GitHub issue type**, not a label — set it with
`gh issue create --type` or `gh issue edit --type`.

| Type | Use when | Not this when |
|------|----------|---------------|
| `Decision` | A choice must be made and recorded before work can proceed | The choice is already made and just needs doing → `Task` |
| `Research` | **The deliverable is a finding**, not a change | The deliverable is a change → something below |
| `Bug` | Something behaves wrong against a stated expectation | Nothing was ever promised → `Feature` |
| `Feature` | A new capability | It is a defect against something promised → `Bug` |
| `Task` | **The deliverable is a change** with an obvious done state — chores, cleanups, test gaps, rollouts, bookkeeping | The deliverable is a finding → `Research` |
| `Epic` | A set of independently-deliverable children, plus the guarantee that the set is **coherent and complete**. **Orthogonal** — never competes with the rows above | It ships as one unit → whatever it actually is |

**When two rows fire, the higher one wins.** The table is in precedence order:
`Decision` → `Research` → `Bug` → `Feature` → `Task`. An issue that both
reports a contradiction *and* requires choosing how to resolve it is a
`Decision`. An issue that is both a rollout and an open question is `Research`.

`Task` and `Research` are separated on **one axis only — the deliverable.** A
verification chore whose outcome is unknown is `Research`, because what it
produces is a finding, even though it has an obvious done state.

**The vocabulary is closed. Never invent a type.** If nothing fits, use the
nearest match and say so in the body.

**Three of these may not exist yet.** `Bug`, `Feature` and `Task` ship with
every org. **`Research`, `Decision` and `Epic` must be created** and may not
be available where you are. If `gh issue create --type` rejects the type,
**leave the type unset, stay at `stage: triage`, and name the intended type in
the body** — never substitute a wrong type that happens to exist. Check with:

```bash
gh api /orgs/<org>/issue-types --jq '.[].name'
```

**There is no `Idea` type.** "Idea" is not a kind of thing — it is a
*commitment level*, and commitment is what stage tracks. An unvalidated
feature proposal is `Feature` at `stage: triage`. If you cannot yet tell what
kind of thing it is, leave the type unset and stay at `stage: triage` —
deciding the type is what triage is for.

**Never name a type after a workflow step.** An issue needing divergent
research is `Research` at `stage: shaping` — never a type called
`divergent-research`. The type says what the issue *is*; the stage says where
it *is*.

### Hierarchy — native sub-issues, not a naming convention

`Epic` describes structure, not kind, which is why it never competes in the
precedence order — an epic is *also* a `Feature`, a `Task`, or whatever its
contents deliver. Use real sub-issues:

```bash
gh issue create --title "..." --parent 42     # file under an epic
gh issue edit 57 --add-sub-issue 61           # attach an existing issue
gh issue view 42 --json subIssues             # read the children
```

An `Epic` may legitimately have no children yet — that is what `drafting` is
for. Each child should deliver value on its own; the epic's job is to make
the set add up to a complete package, which is what its `review` checks. A
tracker that coordinates work without shipping anything itself is an `Epic`.

### 3. Area — what part of the system?

`area: <thing>` labels, defined **per repo**. Deliberately not standardised
across the family: `area: dispatcher` in one repo and `area: tutoring` in
another have nothing to do with each other.

Use an existing one. Only propose a new area when three or more issues would
carry it.

### 4. Priority

| Label | Means |
|-------|-------|
| `priority: p0` | Drop other work. Something is broken or blocking now |
| `priority: p1` | Next up. Ahead of unlabelled work |
| *(no label)* | Normal. **This is most issues** |
| `priority: p2` | Accepted and wanted, ranked below normal |

Do not label normal-priority work. An unlabelled issue is the default, not an
oversight.

### 5. Status — what is true right now?

Additive, and only when true. Closed vocabulary, four bare tokens.

- `blocked` — cannot proceed for a reason that is **not another issue**
  (waiting on a vendor, a credential, an external release). Name it in the
  body. **Issue-to-issue blocking is a native dependency, not this label** —
  see below
- `needs-human` — requires a person; an agent must not proceed alone
- `needs-design-system` — waiting on an upstream design-system change
- `deferred` — accepted and still wanted, but deliberately not scheduled
  **until a stated condition**. Name the condition in the body

**Use the most specific one that applies, and never add `blocked` on top.**
`needs-human` and `needs-design-system` are specific forms of blocked;
`blocked` is the general form for everything else. They do not combine.

### Blocked by another issue — use the native dependency

Do not encode an issue-to-issue edge as a label plus a prose link. It is a
real, queryable, directed relationship:

```bash
gh issue create --title "..." --blocked-by 42
gh issue edit 57 --add-blocked-by 42      # --remove-blocked-by to clear
gh issue list --json number,title,blockedBy
```

The `blocked` label is only for blockers that are **not** issues.

### "Not now" — three states, one question each

Distinct, and the test is mechanical:

| | Has it been accepted? | Consequence |
|---|---|---|
| `stage: triage` | **No** — nobody has committed to it | no priority, no `deferred` |
| `priority: p2` | Yes, ranked low | competes for time, just badly |
| `deferred` | Yes, but waiting on a **stated condition** | does not compete until the condition holds |

If you cannot name the condition, it is not `deferred` — it is `priority: p2`.
If nobody has agreed to do it at all, it is neither; it is `stage: triage`.

## Closing

Always give a reason: `gh issue close --reason completed|not-planned`.
`not-planned` covers won't-do, duplicate, and stale. Link the survivor in a
comment before closing a duplicate. Strip the `stage:` label on close.

## Searching

Because the metadata is structured, search it directly:

```bash
gh issue list --type Bug --label "priority: p0"
gh issue list --label "stage: triage"                             # the untriaged pile
gh issue list --type Decision --label "stage: drafting"
gh issue list --label "stage: ready" --json number,title,labels   # agent-dispatchable
gh search issues --owner <org> --include-prs=false "type:Bug"     # across the family
```

## Legacy issues

Many existing issues still carry `[bracket]` prefixes or superseded labels.
**Never copy them onto a new issue.** On an issue you are already editing for
another reason, normalising it to this convention is **permitted, not
required**. Converting the backlog wholesale is a separate exercise under its
own approval, with its own mapping table — never something to start from here.

## Full reference

`reference/taxonomy.md` — the rationale behind each dimension, the
type-versus-stage distinction, and the questions still open. Read it when a
case does not fit the summary above.
