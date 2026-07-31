# The kodhama issue taxonomy — full reference

The long form behind `SKILL.md`: why each dimension exists, and what is still
open. The legacy mapping is **not** here — it is a one-time migration exercise
that rides `kodhama-0026` and is deliberately kept out of standing agent
context.

Where this document and `SKILL.md` disagree, `SKILL.md` wins — it is the
operative text.

---

## 1. Why this exists

A scan of the live kodhama repos (July 2026; retired Spore excluded) found:

- **Labels were not the problem — they were unused.** Six of the nine live
  repos carried GitHub's stock nine labels, untouched.
- **The real carrier was a `[bracket]` prefix in the title**, holding **eight
  orthogonal dimensions in one slot**: kind, workflow stage, priority, triage
  state, hierarchy, routing, provenance, and area — with inconsistent casing
  and a second, competing `prefix:` form.
- **`(none)` was the most common prefix in four of the nine.**
- **One repo double-encoded kind**: a `[bug]` title prefix *and* a `bug`
  label — 21 prefixes against 11 labels.

One slot cannot carry eight dimensions. That is the whole diagnosis.

**Method note, so §1 is checkable.** A "prefix" means a leading `[bracket]`
**or** a leading `word:` before the first space.

**A measured fact that bears on cost.** The org has `Task`, `Bug` and
`Feature` provisioned, and **not one issue carries a type — 0 of ~296**,
counted across all nine live repos on 2026-07-31 with pull requests excluded.
The denominator drifts daily; the zero has been reproduced independently four
times. Two earlier drafts got this wrong in opposite directions — one claimed
a repo already used native types, the other reported 465, which had counted
pull requests.

## 2. Why native types, not labels

- **Issue Types** are GA and org-level. One type per issue is enforced.
- **Sub-issues** are GA, replacing `[Epic]`/`[Story]`/`[program]`.
- **Issue dependencies** are GA (`--blocked-by`/`--blocking`). An
  issue-to-issue blocker is a native edge, never a label plus a prose link.
- **`--duplicate-of`** records a duplicate as an edge, not a comment.
- **Issue Fields** went to public preview in May 2026 with `Priority`,
  `Effort`, `Start date` and `Target date` preconfigured.

**This taxonomy uses only the GA surface.** Priority is a label, not an Issue
Field, because Fields is still public preview. When Fields reaches GA,
`priority: *` migrates into it and **`kodhama-0026` is superseded, not
edited** — the obligation is the record's, per its Decision 8.

**Provisioning is a precondition, not an edge case.** Three of the six types
must be created *and enabled* before the convention is in force.

## 3. Type vs. stage — the distinction that matters

`[divergent-research]` named a **workflow step** as if it were a kind of
issue. A research issue is `Research` for its whole life; the step it is in
changes. Encoding the step as identity means an issue that finishes research
has a now-lying name, and renaming a step becomes a whole-backlog migration.

**Type is what the issue *is*; stage is where it *is*.**

## 4. The dimensions

### Type — exactly one, precedence-ordered

`Epic` → `Decision` → `Research` → `Bug` → `Feature` → `Task`.

Every value sits on the same single-valued native field, so there are no
"orthogonal" types, only precedence. `Epic` leads, but its row is
**conjunctive** — children *and* coherence-of-the-set as its own deliverable —
so a bucket of unrelated follow-ups never reaches the tie-break.

`Bug` covers artifact-against-artifact contradiction, not only running
behaviour, and not only vertical conflict. The threshold against `Decision` is
whether the correct state is derivable from the upstream.

`Task` and `Research` are drawn on **one axis: the deliverable.**

### Stage — `triage | ready | active | review`

**Four values, one path, every type.** An earlier draft had six values and
per-type paths, which produced two defects a practitioner review named
directly: `shaping` and `drafting` are grove's artifact pipeline, and mean
nothing in four of the nine repos; and the per-type table put `Decision`'s
`ready` before its `drafting`, an inversion that was rewritten twice and
flagged in two rounds. Collapsing removes the table, the inversion, and two
labels per repo.

What was lost is real and worth naming: **the issue can no longer distinguish
"being shaped" from "contract being written".** Grove runs still track that
internally; the backlog does not, on the grounds that eight of nine repos were
never going to.

`triage` is now *not yet dispatchable* rather than *not yet accepted* — it
covers both "noticed" and "accepted but still being worked out". The
commitment moment is leaving it.

Every value names **how far an issue has got**, not what anyone is doing right
now, which is what lets a `deferred` issue keep the stage it reached.

**An `Epic`'s stage is its own and is never derived from its children** — at
any stage, not only one. An earlier draft asserted the independence and then
defined two values in terms of the children.

### Facing — `facing: user` · `facing: system`

**The boundary is this repository's output.** `facing: user` means the change
alters what a consumer of this repo gets; `facing: system` means it changes
only how this repo is built or maintained. **Who maintains the consumer is
irrelevant** — which is what makes it decidable where sibling repos share
maintainers. Two earlier drafts keyed the values on different boundaries.

Set on `Bug`, `Feature` and `Task`. `Decision`, `Research` and `Epic` are
exempt by the same test.

**Kept mandatory against a review recommendation.** A practitioner argued it
does not partition grove, trellis or wisp — nearly everything there is
`facing: user` by the repo-output test — and should be optional there. The
reviewer marked that claim as inference rather than measurement, and it was
not adopted: a uniformly-`user` repo is still answering the question, and an
optional dimension decays to an unused one. **Revisit if measurement shows the
split is genuinely absent.**

### Severity — `session-blocker | broken-feature | papercut`

Required on `Bug`. **Severity is impact; priority is urgency**, and they are
independent: a papercut on the first screen every user sees can be urgent, and
a session-blocker in an unreleased feature can be unprioritised.

This vocabulary is not invented. It is the required dropdown in math-quest's
existing `bug-report.yml`, in daily use before this convention existed — the
team was already recording impact, and an earlier draft of the mapping
discarded it by collapsing `[papercut]` into `priority: p2`.

Values are defined generically so they carry outside a product repo:
"someone is blocked right now" rather than "a kid's session".

### Area — `area: *`, repo-local

**Deliberately not standardised across the family**, including by the seeding
script, which provisions no `area:` label at all. Three-issue minimum.

### Priority — `urgent | high | (unset) | low`

Words, not `p0`/`p1`/`p2`. A numbered scale reads as monotone, so
`p0 < p1 < unlabelled < p2` is a trap — the unlabelled default sits *between*
two numbered values, which no reader expects. The legacy vocabulary said
`low`, and it said what it meant.

### Status — `blocked` · `needs-human` · `deferred`

Three bare tokens. **Status is not a namespace**, deliberately: an earlier
draft wrote `needs: design-system`, a namespace-of-one inside a closed
vocabulary, which invited coining `needs: grove` by analogy.

**`needs-design-system` was then cut entirely.** It hardcoded one sibling repo
into an org-wide vocabulary, and the thing it expressed — waiting on an
upstream change in another repo — is exactly what the native `--blocked-by`
edge carries, cross-repo included. The migration mapping had already conceded
its six legacy uses point the *opposite* direction.

`blocked` and `deferred` differ in kind, not degree: blocked means the work
*cannot* proceed, deferred means it *could* and we chose not to schedule it.

**Any status label suspends dispatch**, and the issue keeps its stage.

### "Not now" — the discriminator

Committed to? No → `triage`. Yes and ranked low → `priority: low`. Yes but
waiting on a **nameable condition** → `deferred`. If you cannot name the
condition, it is `low`.

## 5. Settled: why there is no `Idea` type

Settled against the corpus — 38 issues carrying `[consider]`, `[idea]`, or
`idea:`.

**They are the same thing — repo dialect.** One repo says `consider` (14 uses,
against 2 of `idea`); another says `idea` (17, no `consider`). Outcomes are
indistinguishable: 29% of `consider` closed completed, against 25% of `idea`.

**Neither is a type.** Both span every kind of work.

**The decisive evidence: 10 of the 38 closed as COMPLETED.** A category that
dissolves the moment work finishes is not a kind of thing; it is a position in
a lifecycle. Were `Idea` a type, every idea that shipped would need its type
rewritten on completion.

**This is also why `Epic` survives where `Idea` does not**: an idea that ships
stops being an idea; a container that completes is still a container.

## 5a. Settled: why there is no `Story` type

`[Story]` appears 11 times in one product repo, which has no `[feature]` at
all; the two `[feature]` uses are in a different repo with no `[Story]`. The
vocabularies are per-repo, not competing.

`Story` is not a separate type because **the distinction it carries is
`facing:`** — a `Feature` at `facing: user` is a Story, at `facing: system` an
Enabler. As a type it would fire on the same issues as `Feature`.

**And the name has a failure mode worth recording.** Where a type is called
`Story`, work with no consumer gets a fabricated persona so it can be written
in the format. That invents a reader. The cause is having only one available
shape; giving enabler work `facing: system` removes the pressure at its source.

## 5b. Remaining judgment calls

- **Provenance is not a dimension, and does not become one.** "A real user
  asked for this" goes in the body. It gets no label — `kodhama-0026`
  Decision 7 forbids it, and inventing `from: user` would coin exactly the
  namespace-of-one this document condemns above.
- **Routing is not a dimension either.** Cross-repo blocking is a native
  dependency edge.

## 6. Open questions

**6.1 — `roadmap`** (45 uses, one repo, on 22 of its 41 open issues) is a
selection, not a dimension — Projects territory. Deferred, so the backlog
moves under one change at a time. **Note the cost of deferring**: at launch
the convention sits *on top of* a live selection mechanism rather than
replacing it.

**6.2 — Issue Fields is public preview.** Priority stays a label until GA,
then supersede `kodhama-0026` rather than edit it.

**6.3 — Effort, assignees and milestones are absent.** Assignees and
milestones are native and free and simply unmentioned; effort waits on Issue
Fields. Consequence, named by a practitioner review: `stage: ready` is an
undifferentiated queue that a week cannot be planned from.

**6.4 — Nothing enforces this.** No linter, no CI check, no template. The org
gates a plugin validator on every PR touching `plugins/` and would ship its
filing convention as unenforced prose.

**6.5 — Templates.** Deliberately not owned here; see `../../../DIRECTION.md`
and stewards#65. Templates are transferable across surfaces and belong with
the abstract role; only their projection is GitHub-specific.

**6.6 — Whether existing issues get migrated at all.** The mapping rides
`kodhama-0026`; it does not authorise the edit.

---

## Revision note

Kept short and last: superseded rules stated in the same voice as live ones
are a hazard in standing agent context. Constructs that changed shape across
four adversarial rounds plus a conformance and a practitioner review: `Epic`
(no stage → short path → full path; orthogonal → first in precedence; carries
`facing:` → exempt), `facing:` (added, re-keyed twice, kept mandatory against
a recommendation), the stage vocabulary (`spec`/`building` →
`drafting`/`active` → collapsed to four values and one path), `Decision`
(gained a derivability threshold; its path inversion deleted with the
collapse), `Bug` (widened to non-behavioural and non-vertical conflicts),
`Task` (redrawn on the deliverable axis), priority (`p0/p1/p2` → words),
status (four tokens → three), the close block (twice), and severity (added).
Full history is in the commits and the verdict records on stewards#64.
