# The kodhama issue taxonomy — full reference

The long form behind `SKILL.md`: why each dimension exists, and what is still
open. The mapping from legacy prefixes and labels is **not** here. It is a
one-time migration exercise that rides the ratifying decision and is
deliberately kept out of standing agent context.

Where this document and `SKILL.md` disagree, `SKILL.md` wins — it is the
operative text.

---

## 1. Why this exists

A scan of the live kodhama repos (July 2026; retired Spore excluded) found:

- **Labels were not the problem — they were unused.** Six of the nine live
  repos carried GitHub's stock nine labels, untouched. Only three had ever
  added one.
- **The real carrier was a `[bracket]` prefix in the title**, and it was
  holding **eight orthogonal dimensions in one slot**: kind, workflow stage,
  priority, triage state, hierarchy, routing, provenance, and area — with
  inconsistent casing and a second, competing `prefix:` form.
- **`(none)` was the most common prefix in four of the nine** — trellis
  26/35, grove 31/76, stewards 9/16, wisp 7/11.
- **One repo double-encoded kind**: a `[bug]` title prefix *and* a `bug`
  label — 21 prefixes against 11 labels.

One slot cannot carry eight dimensions. That is the whole diagnosis.

**Method note, so §1 is checkable.** A "prefix" means a leading `[bracket]`
**or** a leading `word:` before the first space — both forms were counted.

**A measured fact that bears on cost.** The org has `Task`, `Bug` and
`Feature` provisioned as native issue types, and **not one issue in the org
carries a type — 0 of 294**, counted across all nine live repos on
2026-07-31 with pull requests excluded. The native dimension is available and
entirely unadopted. Two earlier drafts got this wrong in opposite directions:
one claimed a repo already used native types (false), the other reported a
denominator of 465 (which had counted pull requests, and exceeded the org's
whole issue population). The conclusion is unchanged and the correct figure is
smaller and cleaner.

## 2. Why native types, not labels

GitHub shipped most of this natively, and re-implementing it in labels would
be building a worse copy:

- **Issue Types** are GA and org-level. One type per issue is enforced — a
  label scheme cannot enforce that.
- **Sub-issues** are GA, replacing `[Epic]` / `[Story]` / `[program]` with
  real hierarchy that renders in the UI and rolls up in Projects.
- **Issue dependencies** are GA (`--blocked-by` / `--blocking`). An
  issue-to-issue blocker is a native edge, never a label plus a prose link;
  the `blocked` label survives only for blockers that are not issues.
- **Issue Fields** went to public preview for all orgs in May 2026, with
  `Priority`, `Effort`, `Start date` and `Target date` preconfigured.

**This taxonomy uses only the GA surface** — types, sub-issues, dependencies,
and labels. Priority is a label, not an Issue Field, because Issue Fields is
still public preview and a convention should not be built on unsettled
ground. When Fields reaches GA, `priority: *` migrates into it and this
document is superseded, not edited.

**Provisioning is a precondition, not an edge case.** Three of the six types
must be created before the convention is in force. An earlier draft told
agents to leave the type unset and stay at `stage: triage` when a type was
missing — which, combined with "type required once out of triage", was a
permanent pin that parked accepted work in the disposable pile. `SKILL.md`
now says to stop and report instead.

Prior art consulted: the namespaced-label pattern used by
[IPFS](https://github.com/ipfs/community/blob/master/ISSUE_LABELS.md) and
[github-standard-labels](https://github.com/yoshuawuyts/github-standard-labels).
The namespacing is borrowed; the type dimension is not, because GitHub now
does it natively and better.

## 3. Type vs. stage — the distinction that matters

The most common error in the legacy data was collapsing these.
`[divergent-research]` named a **workflow step** as if it were a kind of
issue. A research issue is `Research` for its whole life; the step it is in
changes. Encoding the step as identity means an issue that finishes research
has a now-lying name, renaming a step becomes a whole-backlog migration, and
the backlog depends on the workflow's vocabulary rather than the reverse.

**Type is what the issue *is*; stage is where it *is*.** The workflow owns the
mapping from `(type, stage)` to its next step.

## 4. The dimensions

### Type — exactly one, precedence-ordered

`Epic` → `Decision` → `Research` → `Bug` → `Feature` → `Task`.

The order exists because real issues match more than one row, and every value
sits on the same single-valued native field — so there are no "orthogonal"
types, only precedence. `Epic` leads, but its row is **conjunctive**: children
that ship separately *and* coherence-of-the-set as its own deliverable. A
bucket of unrelated follow-ups satisfies the first and not the second, so it
never reaches the tie-break at all.

`Bug` covers artifact-against-artifact contradiction, not only running
behaviour — the dominant shape in this corpus. The threshold against
`Decision` is whether the correct state is derivable from the upstream: if it
is, the contradiction is a `Bug`; if resolving it requires choosing, it is a
`Decision`. That threshold is in `SKILL.md`'s operative table, not only
here.

`Task` and `Research` are drawn on **one axis: the deliverable** — a finding
or a change. An earlier draft also gave `Task` an "obvious done state"
criterion, which is a different axis and crossed the first: a verification
chore satisfies both and neither rule resolved it.

Unset is legitimate **only** at `stage: triage`, where deciding the type is
the work.

### Stage — `triage|shaping|drafting|ready|active|review`

Mutually exclusive; exactly one on every open issue **you file**. On an issue
edited for some other reason it is permitted, not required — an unqualified
corpus invariant would license exactly the backlog sweep this convention
forbids. `triage` is the pre-acceptance pile.

**Per-type paths.** `Decision` skips `active` (writing the record *is* the
work, so `drafting` is its working stage); `Research` skips `drafting` (the
work *is* the finding). Everything else takes the full path. **`ready` always
sits immediately before the stage where the work happens** — which is why
`Decision`'s runs `shaping → ready → drafting`, not the reverse.

`stage: ready` is the dispatch signal, but it is **not sufficient on its own**:
an issue also carrying `needs-human`, `blocked` or `deferred` is not
dispatchable, and the query in `SKILL.md` excludes them.

**Stage marks how far an issue has got, not what is happening this minute.**
That is what lets a `deferred` issue keep the stage it reached instead of
needing a stage of its own.

**An `Epic`'s stage is its own and is never derived from its children** — at
any stage, not only `active`. Every value describes the epic's own work:
`drafting` is its breakdown work, `review` its completeness check. An epic
whose coordination is finished is at `review` even with children still open,
and an epic at any stage may hold children at any mix of stages. An earlier
draft asserted the independence and then defined two of the values in terms
of the children, which is why this is stated twice.

### Facing — `facing: user` · `facing: system`

**The boundary is this repository's output.** `facing: user` means the change
alters what a consumer of this repo gets — a product's users, or another
repository that installs or depends on it. `facing: system` means it changes
only how this repo is built or maintained. **Who maintains the consumer is
irrelevant**, which is what makes it decidable in a family where sibling repos
share maintainers.

Two earlier drafts keyed the two values on different boundaries — "outside
this repo" against "outside the team" — which are not complements here. The
repo-output boundary is one test, applied in both directions.

**Why this earns a dimension when provenance and routing did not.** Those
recorded where an issue came from, which changes nothing about the work.
Facing changes how the title is written and whether shipping it is observable
outside the building team. It also cuts *inside* every delivery type rather
than between them, so it cannot be a type without multi-matching. It is set on
the delivery types only — `Bug`, `Feature`, `Task`, `Epic`; a `Decision`
produces a record and a `Research` issue a finding, neither of which is a
change a consumer receives.

The evidence is in the corpus: two issues carried the same `[chore]` label in
the same repo — a duplicated reducer branch, and a theme glyph rendering flush
against a name. The first is invisible outside the team; the second is a
learner looking at a wrong-looking screen.

### Area — `area: *`, repo-local

**Deliberately not standardised across the family**, including by the seeding
script, which provisions no `area:` label at all. Three-issue minimum before
adding one.

### Priority — `p0` · `p1` · *(unset)* · `p2`

Unset is the default and the majority case.

### Status — `blocked` · `needs-human` · `needs-design-system` · `deferred`

Four bare tokens. **Status is not a namespace**, deliberately: an earlier
draft wrote `needs: design-system`, a namespace-of-one inside a closed
vocabulary, which invited agents to coin `needs: grove` by analogy.

`needs-human` and `needs-design-system` are **specific forms of blocked**, not
additions to it. `blocked` and `deferred` differ in kind, not degree: blocked
means the work *cannot* proceed, deferred means it *could* and we chose not
to schedule it.

### "Not now" — the discriminator

`stage: triage`, `priority: p2` and `deferred` all read as "not now" and were
once separated only by a negation. The test is acceptance, then condition:
not accepted → `triage`; accepted and ranked low → `p2`; accepted but held
against a **nameable condition** → `deferred`. If you cannot name the
condition, it is `p2`.

## 5. Settled: why there is no `Idea` type

Settled against the corpus — 38 issues carrying `[consider]`, `[idea]`, or
`idea:`.

**They are the same thing — repo dialect.** One repo says `consider` (14
uses, against 2 of `idea`); another says `idea` (17, no `consider`). Outcomes
are indistinguishable: 29% of `consider` closed completed, against 25% of
`idea`.

**Neither is a type.** Both span every kind of work — decisions, defects,
tasks and coordination containers all appear under both words.

**The decisive evidence: 10 of the 38 closed as COMPLETED** — six `idea`,
four `consider`. A category that dissolves the moment work finishes is not a
kind of thing; it is a position in a lifecycle. Were `Idea` a type, every idea
that shipped would need its type rewritten on completion.

So both words name a **commitment level**, and commitment is what stage
tracks. `stage: triage` is the pre-acceptance stage.

**This is also why `Epic` survives where `Idea` does not**: an idea that ships
stops being an idea; a container that completes is still a container.

## 5a. Settled: why there is no `Story` type

The family's most developed practice used `[Story]` — 11 uses in one product
repo, which has no `[feature]` at all. The two `[feature]` uses are in a
different repo which has no `[Story]`. So the vocabularies are per-repo, not
competing within one.

`Story` is not a separate type, because **the distinction it carries is
`facing:`**. A `Feature` at `facing: user` is a Story; at `facing: system`, an
Enabler. As a type it would fire on the same issues as `Feature`, reviving
the multi-match the precedence order exists to remove.

**And the name has a failure mode worth recording.** Where a type is called
`Story`, work with no consumer gets a fabricated persona so it can be written
in the format — *"as a frontend developer I want to consume an API"*. That
invents a reader, which is the same class of defect as a guessed label. The
cause is having only one available shape; giving enabler work `facing: system`
removes the pressure at its source, which a type name alone could not do.

`[Story]` maps to `Feature · facing: user`, as a child of its epic.

## 5b. Remaining judgment calls

- **Provenance is not a dimension.** "A real user asked for this" goes in the
  body. If it must be filterable, add `from: user` explicitly.
- **Routing is not a dimension either.** Cross-repo blocking is a native
  dependency edge; nothing else routed.

## 6. Open questions

**6.1 — `roadmap`** (45 uses, one repo) is a selection, not a dimension —
Projects territory. Deferred until this taxonomy is ratified, so the backlog
moves under one change at a time. A named exemption, not an oversight.

**6.2 — Issue Fields is public preview.** Priority stays a label until GA,
then supersede this document rather than edit it.

**6.3 — Whether existing issues get migrated at all.** The migration mapping
rides the ratifying decision; it does not authorise the edit.

---

## Revision note

Kept short and last, deliberately: superseded rules stated in the same voice
as live ones are a hazard in standing agent context. Three constructs changed
shape under review — `Epic` (no stage → short path → full path, and orthogonal
→ first in precedence), `facing:` (added, then given a single boundary), and
the stage vocabulary (`spec`/`building` → `drafting`/`active`). The reasoning
for each is folded into §4 above rather than narrated here. Full history is in
the commits and in the verdict records on stewards#64.
