# The kodhama issue taxonomy — full reference

The long form behind `SKILL.md`: why each dimension exists, and what is still
open. The mapping from legacy prefixes and labels is **not** here. It is a
one-time migration exercise that rides the ratifying decision and is
deliberately kept out of standing agent context.

---

## 1. Why this exists

A scan of the live kodhama repos (July 2026; retired Spore excluded) found:

- **Labels were not the problem — they were unused.** Six of the nine live
  repos carried GitHub's stock nine labels, untouched. Only three had ever
  added one.
- **The real carrier was a `[bracket]` prefix in the title**, and it was
  holding **eight orthogonal dimensions in one slot**: kind, workflow stage,
  priority, triage state, hierarchy, routing, provenance, and area — with
  inconsistent casing (`[Story]`, `[Epic]`, `[Decide]` capitalised, the rest
  not) and a second, competing `prefix:` form.
- **`(none)` was the most common prefix in four of the nine** — trellis
  26/35, grove 31/76, stewards 9/16, wisp 7/11. Most issues carried no signal
  at all.
- **One repo double-encoded kind**: a `[bug]` title prefix *and* a `bug`
  label. Two homes for one fact is two chances to drift.

One slot cannot carry eight dimensions. That is the whole diagnosis.

**Method note, so §1 is checkable.** A "prefix" here means a leading
`[bracket]` **or** a leading `word:` before the first space — both forms were
counted, which is why the two competing forms are visible above.

**A measured fact that bears on cost.** The org has `Task`, `Bug` and
`Feature` provisioned as native issue types, and **not one issue carries a
type** — 0 of 465 sampled across six repos on 2026-07-31. The native
dimension is available, not adopted. An earlier draft of this document
claimed a repo triple-encoded kind including a native type; that was wrong,
and it understated the rollout cost of the type dimension to zero when it is
in fact the whole corpus.

## 2. Why native types, not labels

GitHub shipped most of this natively, and re-implementing it in labels would
be building a worse copy:

- **Issue Types** are GA and org-level. One type per issue is enforced — a
  label scheme cannot enforce that.
- **Sub-issues** are GA. They replace `[Epic]` / `[Story]` / `[program]` with
  real hierarchy that renders in the UI and rolls up in Projects.
- **Issue dependencies** are GA (`--blocked-by` / `--blocking`, with
  `blockedBy` / `blocking` in the JSON). An issue-to-issue blocker is a native
  edge, never a label plus a prose link; the `blocked` label survives only for
  blockers that are not issues. Adopted by maintainer direction 2026-07-31 —
  the earlier prose-link form was exactly the "worse copy" this section warns
  against.
- **Issue Fields** (single-select / text / number / date, org-wide, pinnable
  per type) went to public preview for all orgs in May 2026, with `Priority`,
  `Effort`, `Start date` and `Target date` preconfigured.

**This taxonomy deliberately uses only the GA surface** — types, sub-issues,
dependencies, and labels. Priority is a label, not an Issue Field, because
Issue Fields is still public preview and a convention should not be built on
unsettled ground. When Fields reaches GA, `priority: *` migrates into it and
this document is superseded, not edited.

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
it is currently in changes. Encoding the step as the identity means:

- an issue that finishes research has a now-lying name;
- renaming a workflow step becomes a whole-backlog migration;
- the backlog depends on the workflow's internal vocabulary rather than the
  reverse.

So: **type is what the issue *is*; stage is where it *is*.** The workflow owns
the mapping from `(type, stage)` to its next step. That mapping lives with the
workflow, changes with it, and touches no backlog when it does.

## 4. The dimensions

### Type — native issue type, exactly one, precedence-ordered

`Decision` → `Research` → `Bug` → `Feature` → `Task`, with `Epic` orthogonal.

The order exists because real issues match more than one row. A record that
is internally contradictory is both a defect against a stated expectation
*and* a choice that must be made — `Decision` wins, because until the choice
is made there is nothing to fix. A capability that exists in one repo and not
three is both a `Feature` and a rollout `Task` — `Feature` wins, because the
rollout is how it gets delivered, not what it is.

`Task` and `Research` are drawn on **one axis: the deliverable.** An earlier
draft drew `Task` by shape ("an obvious done state") and rejected it by
epistemics ("the outcome is unknown"), which are different axes that cross —
a verification chore satisfies both and neither rule resolved it.

Unset is legitimate **only** at `stage: triage`, where deciding the type is
the work — or where the type is correct but not yet provisioned in the org.

### Stage — `stage: triage|shaping|drafting|ready|active|review`

Mutually exclusive; exactly one on any issue filed or touched under this
convention. `triage` is the pre-acceptance pile.

**Two values were renamed and the universal path was replaced by per-type
paths.** `spec` and `building` were written in the language of a code change,
which left three of six types unstageable: a `Decision` is never built, a
`Research` issue's deliverable is a finding, and an `Epic`'s children sit at
different stages by construction while stage is exclusive. The vocabulary is
now `drafting` and `active`, and each type declares which stages it visits —
so skipping one is correct rather than an omission. See `SKILL.md` for the
per-type table.

**On `Epic` specifically.** An intermediate draft gave `Epic` no stage at all,
on the reasoning that its children carry them. That was wrong, and wrong in a
way this document should have caught: §5 removes `Idea` as a type precisely
because **commitment level belongs on stage** — and a stageless `Epic` cannot
express commitment level, which reintroduces the same defect under a new name.
A container nobody has agreed to and a container being actively filled are
different states. Worse, an `Epic` with no children yet would have had
*nothing* carrying a stage, making it invisible to every stage query including
the triage pile it belongs in.

The reviewer's actual finding was **derivation ambiguity** — max of children,
min, none? The repair is to remove the derivation, not the field: an `Epic`'s
stage is its own and is never computed from its children. There is then no
function to choose.

A second draft gave `Epic` a shortened path on the reasoning that it is never
dispatched as a unit. Also wrong, and it rested on a weak definition. An
`Epic` is not a passive container: it is a set of independently-deliverable
children **plus the guarantee that the set is coherent and complete**. That is
a deliverable, so it has its own defining artifact — the breakdown — and an
agent can be dispatched to produce it. `Epic` therefore takes the full path,
and the per-type table loses a special case.

The invariant is scoped to issues you handle, not asserted over the whole
corpus — an unqualified corpus invariant would license exactly the backlog
sweep this convention forbids.

`stage: ready` is the agent-dispatch signal. It lives on the issue rather than
on a project board deliberately: agents query issues, and a label travels with
the issue everywhere, while a project field only exists inside that project.

### Facing — `facing: user` · `facing: system`

Set on `Feature`, `Bug` and `Task`. "User" means whoever consumes the repo —
a learner for a product, a consuming repository for a plugin.

**Why this earns a dimension when provenance and routing did not.** Those two
recorded where an issue came from, which changes nothing about the work.
Facing changes three things: how the title is written, who can validate that
it is done, and whether shipping it is visible outside the team. It also
cuts *inside* every delivery type rather than between them, so it cannot be a
type without multi-matching.

The evidence it is load-bearing is in the corpus. Two issues carried the same
`[chore]` label in the same repo: untracking a `node_modules` symlink, and a
theme glyph rendering flush against a name. The first is invisible outside
the team; the second is a learner looking at a wrong-looking screen. Nothing
in the legacy scheme separated them. The same split appears in an infra repo,
where "a consumer faces a wall of red checks" is an outward-facing chore
whose user is another repository.

### Area — `area: *` label, repo-local

**Deliberately not standardised across the family**, including by the seeding
script, which provisions no `area:` labels at all. A shared area vocabulary
would be meaningless: one repo's components and another's features have no
relationship. Three-issue minimum before adding one.

### Priority — `priority: p0` · `priority: p1` · *(unset)* · `priority: p2`

Unset is the default and the majority case. Only elevated (`p0`, `p1`) or
explicitly deprioritised (`p2`) work carries a label.

### Status — `blocked` · `needs-human` · `needs-design-system` · `deferred`

**Four bare tokens. Status is not a namespace**, and deliberately so: an
earlier draft wrote `needs: design-system`, which put a namespace-of-one
inside a vocabulary declared closed. The `namespace: value` form is reserved
in this document for **open, extensible** vocabularies (`area:`) and for
closed *ordered* ones (`stage:`, `priority:`); using it for a single closed
member invited agents to coin `needs: grove` by analogy.

`needs-human` and `needs-design-system` are **specific forms of blocked**, not
additions to it — they never co-occur with `blocked`. This resolves what was
previously stated two ways: `SKILL.md` called status additive while this
document called `needs-design-system` an alternative to `blocked`.

`needs-design-system` is kept as its own token rather than folded into
`blocked` because the design-system dependency is structural in this family —
the DS reaches consumers only through generation-time links, so "waiting on
DS" is a distinct and recurring condition worth filtering.

### "Not now" — the discriminator

`stage: triage`, `priority: p2` and `deferred` all read as "not now" and were
previously separated only by a negation (*"not the same as low priority"*),
which is not a rule. The test is acceptance, then condition:

1. Not accepted by anyone → `stage: triage`. Neither of the others applies.
2. Accepted, ranked low → `priority: p2`.
3. Accepted, but waiting on a **nameable condition** → `deferred`, condition
   in the body. **If you cannot name the condition, it is `priority: p2`.**

## 5. Settled: why there is no `Idea` type

An earlier draft had `Idea` as a type and left open whether the legacy
`[consider]` and `[idea]` prefixes meant different things. Both were settled
against the corpus — 38 issues carrying `[consider]`, `[idea]`, or `idea:`.

**They are the same thing — repo dialect, not semantics.** One repo says
`consider` (14 uses, against 2 of `idea`); another says `idea` (17 uses, no
`consider`). Their outcomes are indistinguishable: 29% of `consider` issues
closed completed, against 25% of `idea` issues.

**Neither is a type.** Both span every kind of work. Among one repo's
`[consider]` issues alone: #40 and #130 are decisions ("prevent drift *vs.*
detect it", "decide its v0 fate"), #52 and #82 are defects, #78 and #84 are
tasks, and #91 is a coordination container — an `Epic` under this taxonomy,
which covers containers that coordinate without shipping. The other repo's
`[idea]` set is the same mix — #135 a decision, #287 a bug, #344 a task.

**The decisive evidence: 10 of the 38 closed as COMPLETED** — six `idea`,
four `consider`. A category that dissolves the moment work finishes is not a
kind of thing; it is a position in a lifecycle. Were `Idea` a type, every idea
that shipped would need its type rewritten on completion — exactly what a type
must not require.

So both words name a **commitment level**, and commitment is what stage
tracks. `Idea` is removed as a type and `stage: triage` added as the
pre-acceptance stage.

**This is also why `Epic` survives as a type where `Idea` does not**, and the
distinction is principled rather than preferential: the test is whether the
category dissolves on completion. An idea that ships stops being an idea; a
container that completes is still a container.

## 5b. Settled: why there is no `Story` type

The family's most developed practice used `[Story]` (11 uses, against 2 of
`[feature]`), paired with `[Epic]` and an epic-story numbering scheme. The
question was whether `Story` should replace the native `Feature` type.

It should not — but not because the distinction it carries is unreal. That
distinction is now encoded as `facing:`, above. **A `Feature` at
`facing: user` is a Story; at `facing: system`, an Enabler.** What follows is
why it is not a *type*.

The deciding reason is a failure mode of the **name**, not of the concept. Where a type is called `Story`, work with no end user gets a
fabricated persona so it can be written in the format — *"as a frontend
developer I want to consume an API"* is the canonical example. That invents a
reader who does not exist, which is the same class of defect as a guessed
label: a field asserting something untrue. A type name that pressures authors
into fiction is a bad type name.

What `Story` genuinely carries is **independent deliverability**, and that is
not a kind of thing — it is a structural fact already expressed by the
sub-issue relationship. A child of an `Epic` that closes on its own *is*
independently deliverable; a second type would restate hierarchy that
`Epic` + sub-issues already encodes, and would fire on the same issues as
`Feature`, reviving the multi-match ambiguity §4's precedence order removes.

And the cheat has a cause worth naming: **a fabricated persona is what
happens when only one shape is available.** Enabler work invents a reader
because it has nowhere honest to sit. Giving it `facing: system` removes the
pressure at its source, which one type name alone could not do.

`[Story]` maps to `Feature · facing: user`, as a child of its epic.

## 5a. Remaining judgment calls

Flagged so they can be overturned rather than inherited silently.

- **Provenance is not a dimension.** "A real user asked for this" goes in the
  body, not a label. Three legacy occurrences did not justify a ninth
  dimension. If it must be *filterable*, add `from: user` explicitly.
- **Routing is not a dimension either.** Cross-repo dependency is carried by
  status; nothing else routed.

## 6. Open questions

*(6.1, the code-shaped stage vocabulary, was resolved by maintainer direction
on 2026-07-31 — per-type paths plus the `drafting`/`active` renames. See §4.
6.4, native issue dependencies, was resolved in the same act: adopt. See §2.)*

**6.2 — `roadmap`** (45 uses, one repo) is a selection, not a dimension —
Projects territory. Deferred until this taxonomy is ratified, so the backlog
moves under one change at a time. A named exemption, not an oversight.

**6.3 — Issue Fields is public preview.** Priority stays a label until GA,
then supersede this document rather than edit it.

**6.5 — Whether existing issues get migrated at all.** The migration mapping
exists and rides the ratifying decision; it does not authorise the edit.
