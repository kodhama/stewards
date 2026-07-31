---
id: kodhama-0026-issue-taxonomy
type: decision
status: gated  # author self-check recorded. Four independent review rounds have run (90a7bbb, ff1e47c, 7c0c54d, 228e7ed); twelve verdict records on stewards#64; NONE PASSED. This state answers round 4 and is itself unreviewed. The maintainer's intent act remains open and is not opened by an agent
depends_on: [kodhama-0009-org-topology-spirit-stewards-trees, stewards/kodhama-0008-family-inheritance-restate-nothing, stewards/kodhama-0021-separate-adoption-posture-from-support, stewards/kodhama-0022-propagate-collective-strategy]
owner: agent
updated: 2026-07-31
provenance: "shaped 2026-07-30 from a scan of all live kodhama repos; two vocabulary questions settled against the corpus (no Idea type; consider ≡ idea ≡ stage: triage). Independently reviewed 2026-07-31 by decision-adversary (NEEDS-REVISION), spec-adversary (NEEDS-REVISION, on the taxonomy) and corpus-reviewer, all posted to stewards#64; this revision answers them. Placement at the org layer is maintainer direction of 2026-07-30, not a criterion derived from the corpus. On 2026-07-31 the maintainer directed that the kodhama-0021 conflict be resolved by narrowing rather than by superseding 0021; the Done-when was subsequently emptied of delivery criteria altogether, which resolves it more completely than the direction asked. Delivery lives in the wave brief."
---

# Decision: one issue taxonomy for the forest — structured metadata, prose titles

## Why

Issue metadata across the forest has no shared shape. **Six of the nine live
repos carry GitHub's stock labels untouched**; the actual signal rides a
`[bracket]` title prefix which had accumulated **eight orthogonal dimensions
in one slot** — kind, workflow stage, priority, triage state, hierarchy,
routing, provenance, area — in two competing forms with inconsistent casing,
and `(none)` is the most common prefix in four repos. math-quest additionally
double-encodes kind: a `[bug]` title prefix *and* a `bug` label.

The cost is not aesthetic. Nothing is queryable across repos, agent dispatch
has no reliable signal to read, and the same fact drifts between its copies.

**A measured fact that bears on cost.** The org has `Task`, `Bug` and
`Feature` provisioned as native issue types, and **not one issue in the org
carries a type — 0 of ~296**, counted across all nine live repos on 2026-07-31
with pull requests excluded. The native dimension is available and entirely
unadopted. Two earlier drafts got this wrong in opposite directions: one
claimed math-quest already used native types, the other reported 465 — a
denominator that had counted pull requests and exceeded the org's whole issue
population. The conclusion is unchanged; the correct figure is smaller.

## Decision

1. **Issue titles are prose.** No bracket prefixes, no `type:` prefixes.
   Every machine-readable dimension lives in structured metadata.
2. **Kind is the native GitHub issue type** — `Bug`, `Feature`, `Task`
   (provisioned) plus `Research`, `Decision`, `Epic` (to be created). Closed
   vocabulary.
3. **There is no `Idea` type.** "Idea" and "consider" name a commitment
   level, not a kind; commitment is carried by stage. Both become
   `stage: triage`. The discriminating test is that a category which
   dissolves the moment work finishes is a lifecycle position, not a kind —
   which is also why `Epic` **is** a type: a container does not dissolve on
   completion.
4. **Stage, priority, facing, status and area are labels.** Every closed one
   is enumerated in this record — these four here, `facing:` in clause 5 —
   so the closure is enforceable by the record rather than by a file it
   points at:
   - `stage:` — `triage` · `shaping` · `drafting` · `ready` · `active` ·
     `review`. Mutually exclusive. The sequence is the default; a type may
     visit a subset in its own order, which the plugin states
   - `priority:` — `p0` · `p1` · `p2`, with **unset** meaning normal
   - status — `blocked` · `needs-human` · `needs-design-system` · `deferred`.
     Bare tokens; **status is not a namespace**
   - `area:` — **open and deliberately repo-local**, the only open vocabulary

   Which stages each type visits, and every rule for applying these, is the
   plugin's to state. **Membership is this record's.**
5. **`facing: user` / `facing: system`** — a closed pair — records whether
   the change alters what a **consumer of this repository** gets: a product's
   users, or another repository that installs or depends on it. Who maintains
   the consumer is irrelevant. It is a dimension rather than a type
   because it cuts *inside* every delivery type — and it is what lets an agile
   Story and an Enabler be one type seen from two sides, which removes the
   pressure to invent a persona for work that has no consumer.
6. **Hierarchy is native sub-issues**, not `[Epic]`/`[Story]` prefixes.
7. **Routing and provenance are not dimensions.** Issue-to-issue blocking is a
   **native GitHub dependency edge** (`--blocked-by`), not a label and not
   prose; the source of a request is recorded in the issue body. Neither gets
   a label. This closes the last two of the eight dimensions indicted above.
8. **Priority stays a label, not a GitHub Issue Field**, until Issue Fields
   leaves public preview. At its GA this decision is superseded, not edited.
9. **The convention is carried by GitHub itself** — the org's issue types and
   the seeded labels are what make it real, and it is operable the moment they
   exist. A **skill teaches agents to apply it**, and that skill arrives by
   plugin; **repos restate nothing** (`kodhama-0008` §4). No repo hand-authors
   a copy, an index, or a README section; bare pointers to the plugin-carried
   source are permitted. Which plugin carries the skill is a delivery choice
   owned by the wave, not a term of this decision.
10. **Grove owns the mapping from `(type, stage)` to its workflow steps.** No
   issue is named after a grove step. The type says what an issue *is*; the
   stage says where it *is*.
11. **The convention binds the whole forest, trees included. The plugin does
    not.** Adoption of the carrying plugin is each repository's own act, per
    approved `kodhama-0021` — *"Math Quest receives no plugin change until it
    explicitly opts into preview."* This decision makes the taxonomy
    authoritative and available; it does not enable a plugin anywhere.
    Nothing here amends or supersedes `kodhama-0021`.

12. **Between ratification and provisioning the convention is decided but not
    operable.** Until an org creates and enables `Research`, `Decision` and
    `Epic`, the skill's first instruction is to stop, so ratifying this record
    changes no repository's behaviour by itself. The order is decide,
    provision, adopt.

## Propagation (`kodhama-0022`)

Applicable plugin repositories, from the marketplace catalog: **Grove**,
**Trellis**, **Wisp**, and **Stewards** (which carries the `kodhama` plugin
and is downstream here because the upstream record is not its own).
Non-plugin repositories receive no cross-link ADR. The five non-plugin repositories — math-quest, design-system,
sdd-gauntlet, homebrew-tap and kodhama — are reached through ordinary product
ownership, an issue in each, per
`kodhama-0022` §1's "immediate targets are repositories that own an affected plugin" and the
`kodhama-0008` precedent that math-quest's copy "is math-quest's own issue."

**Recorded gap:** `kodhama-0022` names *"the approved Stewards decision"* as
the authority its downstream ADRs must cite. This record sits at the org
layer, so the mechanism is applied here by analogy rather than by its literal
text. See open question 2.

## Done when

This record decides a convention. Its completion test is whether the
convention is decided — **not whether it has been delivered anywhere.**

- Every vocabulary this record calls closed is **enumerated in this record**:
  the six types, the six stage values, the four status tokens, the two
  `facing:` values, and the priority set. A closure the record does not
  enumerate is a closure it cannot enforce.
- The record is ratified by the maintainer's intent act.

**Nothing about delivery is a criterion here.** Publication, org-type
provisioning, cross-link ADRs, math-quest's receiving issue and per-repo
adoption are rollout facts, and rollout completion is the **brief's** ledger
(`conductor/wave-issue-taxonomy.md`, Lanes A–F). An earlier draft listed all
five here while simultaneously disclaiming them — which made an unresolved
plugin home block a decision that has nothing to do with where a plugin
lives.

## Open questions

**1. Where the plugin lives — resolved 2026-07-31, and never a term of this
record.** Maintainer direction: the `kodhama` plugin in Stewards, whose
identity is the family's GitHub operations. Recorded here only because an
earlier draft of Decision 9 made the plugin the sole carrier and so made this
look like a gate. It was not; the convention is carried by the org's types and
labels. The graduation path and the coming abstract/concrete split are in
`plugin/DIRECTION.md`. The three candidates weighed were:
  - the Stewards `kodhama` plugin — but its scope is deliberately narrow
    (CI marketplace setup), and widening it contradicts that narrowness;
  - **grove** — which the standing corpus nominates, since `kodhama-0008` §3
    holds that "operational content is grove's" and Decision 10 already hands
    grove the `(type, stage)` mapping. The cost is that repositories which
    never install grove would not receive the taxonomy — and, sharper, that
    **Trellis is a propagation target while `CLAUDE.md` declares dependency
    direction "strictly downward (wisp → grove → trellis)"**, so a
    grove-carried taxonomy reaches Trellis only by inverting that direction;
  - its own repository on the `git-subdir` pattern — consistent with how
    grove, trellis and wisp are carried, but it adds a node to a topology
    `CLAUDE.md` declares "strictly downward" without saying where it sits.

**2. Whether `kodhama-0022` reaches an org-layer upstream.** Its text names a
Stewards decision as the authority throughout. Either 0022 is amended to
cover org-layer upstreams, or this record's propagation stands on its own
footing. Not blocking — the propagation section above names its targets
either way.

**3. The cross-repo reference grammar is inconsistent, and no ruling exists.**
`.grove/relations.md` says cross-repo `<repo>/<id>` referents "are
**permitted**", and `.grove/versioning.md` defines the qualified form for
`@version` pins. **Neither mandates it, and neither states any grammar for
`depends_on` at all.** An earlier draft of this record called the bare form
"a defect by the declared grammar"; that was inference presented as a ruling,
and it is withdrawn. `kodhama-0022`'s self-check does call the qualified
grammar "settled", but a self-check is not a decision.

The practice, counted across every relation class:

| record | relation → `kodhama-0009` | form |
|---|---|---|
| `decisions/0002` | `superseded_in_part_by` | bare |
| `decisions/0010` | `depends_on` | bare |
| `decisions/0021` | `depends_on` | bare |
| `decisions/0022` | `depends_on` | qualified |
| `kodhama-0009` → `kodhama-0002` | `depends_on` | bare |

**Four of five are bare, and a ruling would settle five existing records**,
not the four an earlier draft counted.

This record's `depends_on` is qualified **for its destination**
(`kodhama/kodhama`) — `kodhama-0009` bare, the three Stewards records
prefixed. That is correct on arrival and **knowingly incorrect while staged
here**, where a walker sees the three resolvable referents marked foreign and
the one foreign referent marked local. It is a deliberate choice and a poor
one to leave standing: **the ruling is what this question asks for, and until
it is made the destination-first form should be set in the relocation commit,
not carried in a field that is wrong where it lives.**

**4. `roadmap`** (45 uses, math-quest only) is a selection, not a dimension —
Projects territory. Deferred until this taxonomy is ratified, so the backlog
moves under one change at a time. A named exemption, not an oversight.

**5. Whether legacy issues are migrated at all.** The mapping exists; this
record does not authorise the edit.

## Self-check (gate)

**Four independent review rounds have run. None passed.** Twelve verdict
records on stewards#64, binding `90a7bbb`, `ff1e47c`, `7c0c54d` and `228e7ed`
— a decision-adversary, a spec-adversary and a corpus-reviewer each round,
dispatched cold. **The current state is not among them and is unreviewed.**

What the rounds found, in order, because the shape of the sequence is itself
disclosure:

1. **A conflict with approved `kodhama-0021`**, uncited — the record required
   plugin enablement in a product repo whose adoption 0021 reserves to its
   maintainer. Plus eight blocking spec findings: undecidable vocabularies,
   two flat internal contradictions, and a stage set undefined for half the
   type table.
2. **The record no longer described the taxonomy it ratifies.** The two had
   been repaired in separate passes and had diverged for five commits. Seven
   further blocking spec findings, all in constructs round 1's repairs had
   introduced.
3. **Stale text beside new text** — a fixed rule next to its unfixed
   neighbour, a renamed thing next to its old name. Six blocking spec
   findings, and four internal cross-references left pointing one clause low
   after a clause was inserted.
4. **The record's account of itself.** Six blocking spec findings; a sentence
   shipped with its predicate deleted; the review history stated three
   incompatible ways. Round 4's reviewer named the recurring cause: repairs
   were made at the point of the reported defect, and passages *depending on*
   the repaired text were not re-walked. The current state was produced with
   the check it proposed — for each construct changed, grep every occurrence
   of its key terms and re-read each hit.

**Four factual errors in the author's own evidence, every one caught by review
rather than by the author:**

- a claim that a repo triple-encoded kind including a native type — **wrong**;
- its replacement, "0 of 465", counted pull requests — **also wrong**. The
  figure is 0 of ~296, reproduced independently three times since;
- `depends_on` used bare cross-repo ids on one record's practice, which the
  author then called *"a defect by the declared grammar"* — an **over-read**:
  the companions say such referents are *permitted*, not mandated, and state
  no grammar for `depends_on` at all. Both claims withdrawn, and open question
  3 now says plainly that no ruling exists;
- an edit deleted a sentence's predicate and shipped the fragment.

**Two corrections of shape, both prompted by the maintainer rather than by a
reviewer** — and both the same mistake, one clause apart. The Done-when
listed five delivery criteria while disclaiming delivery, which made an
unresolved plugin home block a decision about issue classification; it now
tests only whether the convention is decided. And Decision 9 called the plugin
the *sole carrier*, which made the same welding one clause further along; the
convention is carried by the org's types and labels, and the skill teaches it.

**What is settled, and on what.** The two vocabulary questions — no `Idea`
type, no `Story` type — were settled against the corpus rather than by
preference, on 38 issues of which 10 closed COMPLETED; the arithmetic has been
independently reproduced in three separate rounds. Every closed vocabulary the
record declares is enumerated in the record, so the closure is enforceable
here rather than by a file this points at.

**What remains open** is listed above as open questions, and none of it blocks
this record: the plugin home is settled for now as a staging choice, `roadmap`
is a named exemption, Issue Fields waits on GA, the cross-repo grammar wants a
ruling that would bind five records, and migration is unauthorised.

**The author did not grade its own decision and did not open the intent gate.**
