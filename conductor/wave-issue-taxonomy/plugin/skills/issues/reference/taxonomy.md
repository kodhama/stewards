# The kodhama issue taxonomy — full reference

The long form behind `SKILL.md`: why each dimension exists, and what is still
open. The mapping from legacy prefixes and labels is **not** here — it is a
one-time exercise and lives in `migration/legacy-mapping.md`.

---

## 1. Why this exists

A scan of all ten kodhama repos (July 2026) found:

- **Labels were not the problem — they were unused.** Seven of ten repos
  (`trellis`, `spore`, `wisp`, `design-system`, `stewards`, `sdd-gauntlet`,
  `homebrew-tap`) carried GitHub's stock nine labels, untouched. Only `grove`,
  `kodhama`, and `math-quest` had ever added one.
- **The real carrier was a `[bracket]` prefix in the title**, and it was
  holding **eight orthogonal dimensions in one slot**: kind, workflow stage,
  priority, triage state, hierarchy, routing, provenance, and area — with
  inconsistent casing (`[Story]`, `[Epic]`, `[Decide]` capitalised, the rest
  not) and a second, competing `prefix:` form.
- **`(none)` was the plurality in five of ten repos** — trellis 26/35,
  grove 31/76, stewards 9/16, wisp 7/11. Most issues carried no signal at all.
- **`math-quest` double-encoded**: `[bug]` in the title *and* a `bug` label
  *and* a native `Bug` type. Three homes for one fact is three chances to
  drift.

One slot cannot carry eight dimensions. That is the whole diagnosis.

## 2. Why native types, not labels

GitHub shipped most of this natively, and re-implementing it in labels would
be building a worse copy:

- **Issue Types** are GA and org-level. The `kodhama` org already has `Task`,
  `Bug`, and `Feature` provisioned; custom types are creatable. One type per
  issue is enforced — a label scheme cannot enforce that.
- **Sub-issues** are GA. They replace `[Epic]` / `[Story]` / `[program]` with
  real hierarchy that renders in the UI and rolls up in Projects.
- **Issue Fields** (single-select / text / number / date, org-wide, pinnable
  per type) went to public preview for all orgs in May 2026, with `Priority`,
  `Effort`, `Start date`, and `Target date` preconfigured.

**This taxonomy deliberately uses only the GA surface** — types, sub-issues,
and labels. Priority is a label, not an Issue Field, because Issue Fields is
still public preview and a convention should not be built on unsettled
ground. When Fields reaches GA, `priority: *` migrates into it and this
document should be superseded, not edited.

Prior art consulted: the standard namespaced-label pattern
(`Type:` / `Priority:` / `Status:`) as used by
[IPFS](https://github.com/ipfs/community/blob/master/ISSUE_LABELS.md) and
[github-standard-labels](https://github.com/yoshuawuyts/github-standard-labels).
The namespacing convention is borrowed; the type dimension is not, because
GitHub now does it natively and better.

## 3. Type vs. stage — the distinction that matters

The single most common error in the legacy data was collapsing these.

`[divergent-research]` named a **grove workflow step** as if it were a kind of
issue. It isn't. A research issue is `Research` for its whole life; the step
it's currently in changes. Encoding the step as the identity means:

- an issue that finishes research has a now-lying name;
- renaming a grove step becomes a ten-repo backlog migration;
- the backlog depends on grove's internal vocabulary rather than the reverse.

So: **type is what the issue *is*; stage is where it *is*.** Grove's dispatcher
owns the mapping from `(type, stage)` to its next step. That mapping lives in
grove, changes with grove, and touches no backlog when it does.

## 4. The dimensions

### Type — native issue type, exactly one

`Bug` · `Feature` · `Task` (native, already provisioned)
`Research` · `Decision` · `Epic` (custom, need creating)

Unset is legitimate **only** at `stage: triage`, where deciding the type is
the work.

### Area — `area: *` label, repo-local

**Deliberately not standardised across the family.** A shared area vocabulary
would be meaningless: grove's components and math-quest's features have no
relationship. Each repo defines its own; three-issue minimum before adding one.

### Priority — `priority: p0` · `priority: p1` · *(unset)* · `priority: p2`

Unset is the default and the majority case. Only elevated (`p0`, `p1`) or
explicitly deprioritised (`p2`) work carries a label. This keeps the signal
where the signal is.

### Stage — `stage: triage|shaping|spec|ready|building|review`

Mutually exclusive; every open issue carries exactly one. `triage` is the
pre-acceptance pile — see §5.

`stage: ready` is the agent-dispatch signal. It lives on the issue rather than
on a project board deliberately: agents query issues, and a label travels with
the issue everywhere, while a project field only exists inside that project.

### Status — `blocked` · `deferred` · `needs-human` · `needs: design-system`

Additive, only when true. `blocked` requires a linked cause in the body.

`needs: design-system` is kept as its own status rather than folded into
`blocked` because the design-system dependency is structural in this family —
the DS reaches consumers only through generation-time links, so "waiting on
DS" is a distinct and recurring condition worth filtering.

## 5. Settled: why there is no `Idea` type

An earlier draft had `Idea` as a type and left open whether the legacy
`[consider]` and `[idea]` prefixes meant different things. Both were settled
against the corpus — 38 issues carrying `[consider]`, `[idea]`, or `idea:`
across all repos.

**They are the same thing — repo dialect, not semantics.** grove says
`consider` (14 uses, against 2 of `idea`); math-quest says `idea` (17 uses,
no `consider`). Their outcomes are indistinguishable: 29% of `consider`
issues closed completed, against 25% of `idea` issues.

**Neither is a type.** Both span every kind of work. Among grove's
`[consider]` issues alone: #40 and #130 are decisions ("prevent drift *vs.*
detect it", "decide its v0 fate"), #52 and #82 are defects, #78 and #84 are
tasks, #91 is a tracker. math-quest's `[idea]` set is the same mix — #135 is
a decision, #287 a bug, #344 a task.

**The decisive evidence: 10 of the 38 closed as COMPLETED** — six `idea`,
four `consider`. A category that dissolves the moment work finishes is not a
kind of thing; it is a position in a lifecycle. Were `Idea` a type, every
idea that shipped would need its type rewritten on completion — exactly what
a type must not require.

So both words name a **commitment level**, and commitment is what stage
tracks. `Idea` is removed as a type and `stage: triage` added as the
pre-acceptance stage. An unvalidated feature proposal is `Feature` at
`stage: triage`; an untriaged defect is `Bug` at `stage: triage`. Where the
kind genuinely isn't known yet the type stays unset — deciding it *is* the
triage work.

This is why the pipeline gained a stage after the first draft, and why
`roadmap` (§6) was right to wait for it.

## 5a. Remaining judgment calls

Flagged so they can be overturned rather than inherited silently.

- **Provenance is not a dimension.** "A real user asked for this" goes in the
  body, not a label. Three legacy occurrences did not justify a ninth
  dimension. If it needs to be *filterable*, add `from: user` explicitly.
- **`Epic` is a type as well as a sub-issue parent.** Sub-issues alone would
  give the hierarchy, but a type makes containers filterable on their own.

## 6. Open questions

- **`roadmap` (45 uses, math-quest only) has no home in this taxonomy.** It
  is not a dimension — it is a *selection*: "this is on the plan." That is
  what GitHub Projects is for, and a Project would also give ordering and
  rollup a label cannot. **Deliberately deferred until this taxonomy is
  ratified**, so the backlog only moves under one change at a time. Interim:
  keep the label untouched. This is a named exemption, not an oversight.
- **Issue Fields is public preview.** Priority stays a label until GA.
- **Where the ratifying decision lives** — this taxonomy binds `math-quest`
  (a product) as well as the stewards, which reads as org-level rather than
  steward-level.
- **Whether existing issues get migrated at all.** `migration/legacy-mapping.md`
  specifies the mapping; it does not authorise the edit.
