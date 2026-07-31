---
id: kodhama-0026-issue-taxonomy
type: decision
status: gated  # author self-check recorded and three independent reviews returned; the maintainer's intent act remains open and is not opened by an agent
depends_on: [kodhama-0009-org-topology-spirit-stewards-trees, kodhama-0008-family-inheritance-restate-nothing, kodhama-0021-separate-adoption-posture-from-support, kodhama-0022-propagate-collective-strategy]
owner: agent
updated: 2026-07-31
provenance: "shaped 2026-07-30 from a scan of all live kodhama repos; two vocabulary questions settled against the corpus (no Idea type; consider ≡ idea ≡ stage: triage). Independently reviewed 2026-07-31 by decision-adversary (NEEDS-REVISION), spec-adversary (NEEDS-REVISION, on the taxonomy) and corpus-reviewer, all posted to stewards#64; this revision answers them. Placement at the org layer is maintainer direction of 2026-07-30, not a criterion derived from the corpus. The Done-when narrowing to publication-plus-opt-in is maintainer direction of 2026-07-31, taken in preference to superseding kodhama-0021."
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
`Feature` provisioned as native issue types, and **not one issue in the
forest carries a type** — 0 of 465 sampled across six repos on 2026-07-31.
The native dimension is available, not adopted. An earlier draft of this
record claimed math-quest triple-encoded kind including a native type; that
was wrong, and it understated the rollout cost.

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
4. **Stage, priority, status and area are labels.** `stage:` and `priority:`
   are closed namespaced vocabularies; `area:` is an open namespaced
   vocabulary, deliberately repo-local; **status is a closed set of bare
   tokens and is not a namespace**.
5. **Hierarchy is native sub-issues**, not `[Epic]`/`[Story]` prefixes.
6. **Routing and provenance are not dimensions.** Cross-repo dependency is
   carried by status; the source of a request ("a user asked for this") is
   recorded in the issue body. Neither gets a label. This closes the last two
   of the eight dimensions indicted above.
7. **Priority stays a label, not a GitHub Issue Field**, until Issue Fields
   leaves public preview. At its GA this decision is superseded, not edited.
8. **The taxonomy arrives by plugin, and repos restate nothing**
   (`kodhama-0008` §4). No repo hand-authors a copy, an index, or a README
   section. Bare pointers to the plugin-carried source are permitted.
9. **Grove owns the mapping from `(type, stage)` to its workflow steps.** No
   issue is named after a grove step. The type says what an issue *is*; the
   stage says where it *is*.
10. **The convention binds the whole forest, trees included. The plugin does
    not.** Adoption of the carrying plugin is each repository's own act, per
    approved `kodhama-0021` — *"Math Quest receives no plugin change until it
    explicitly opts into preview."* This decision makes the taxonomy
    authoritative and available; it does not enable a plugin anywhere.
    Nothing here amends or supersedes `kodhama-0021`.

## Propagation (`kodhama-0022`)

Applicable plugin repositories, from the marketplace catalog: **Grove**,
**Trellis**, **Wisp**, and **Stewards** (which carries the `kodhama` plugin
and is downstream here because the upstream record is not its own).
Non-plugin repositories receive no cross-link ADR. math-quest is reached
through ordinary product ownership — an issue in math-quest — per
`kodhama-0022` §1's exclusion of non-plugin repositories and the
`kodhama-0008` precedent that math-quest's copy "is math-quest's own issue."

**Recorded gap:** `kodhama-0022` names *"the approved Stewards decision"* as
the authority its downstream ADRs must cite. This record sits at the org
layer, so the mechanism is applied here by analogy rather than by its literal
text. See open question 2.

## Done when

- The plugin carrying the taxonomy skill is **published** to the `kodhama`
  marketplace. **Adoption is not part of this record's completion** — each
  repository opts in by its own act, on its own authority.
- Org issue types `Research`, `Decision` and `Epic` exist. This requires a
  credential with `admin:org`; the maintainer's current token carries
  `read:org` only, so Decision 2's vocabulary is unimplementable until that
  is resolved.
- Cross-link ADRs exist in the four repositories named under Propagation.
- math-quest carries its own receiving issue.
- The rollout brief `conductor/wave-issue-taxonomy.md` is closed with a
  report. Rollout completion is the **brief's** ledger, not this record's.

## Open questions

**1. Where the plugin lives — BLOCKING.** Decision 8 makes the plugin the
sole carrier, so the first Done-when criterion cannot be evaluated until this
resolves. Three candidates, none yet chosen:
  - the Stewards `kodhama` plugin — but its scope is deliberately narrow
    (CI marketplace setup), and widening it contradicts that narrowness;
  - **grove** — which the standing corpus nominates, since `kodhama-0008` §3
    holds that "operational content is grove's" and Decision 9 already hands
    grove the `(type, stage)` mapping. The cost is that repositories which
    never install grove would not receive the taxonomy;
  - its own repository on the `git-subdir` pattern — consistent with how
    grove, trellis and wisp are carried, but it adds a node to a topology
    `CLAUDE.md` declares "strictly downward" without saying where it sits.

**2. Whether `kodhama-0022` reaches an org-layer upstream.** Its text names a
Stewards decision as the authority throughout. Either 0022 is amended to
cover org-layer upstreams, or this record's propagation stands on its own
footing. Not blocking — the propagation section above names its targets
either way.

**3. The cross-repo reference grammar is inconsistent in the corpus.**
`kodhama-0009` (approved, in `kodhama/kodhama`) references the Stewards
record `kodhama-0002` **bare**; Stewards' `kodhama-0022` references `0009` as
`kodhama/kodhama-0009-…`. Three of four cross-repo references in the shared
namespace are bare. This record follows the destination repository's own
precedent and uses bare ids throughout. A ruling would settle four existing
records as well as this one.

**4. `roadmap`** (45 uses, math-quest only) is a selection, not a dimension —
Projects territory. Deferred until this taxonomy is ratified, so the backlog
moves under one change at a time. A named exemption, not an oversight.

**5. Whether legacy issues are migrated at all.** The mapping exists; this
record does not authorise the edit.

## Self-check (gate)

Two vocabulary questions were settled against the corpus rather than by
preference; the evidence — 38 issues examined, 10 of them closed COMPLETED —
is recorded with the taxonomy and was independently checked and confirmed
arithmetically sound by the spec-adversary.

**This revision answers three independent reviews**, all posted to
stewards#64 against commit `90a7bbb`:
- the conflict with approved `kodhama-0021` was real and uncited. Resolved by
  maintainer direction of 2026-07-31: **narrow the Done-when** to publication
  plus repo-owned opt-in, rather than supersede 0021. Decision 10 now states
  the convention/plugin split explicitly;
- the `kodhama-0022` invocation named no targets. A propagation section now
  does, and the mechanism's reach over an org-layer upstream is recorded as
  an open gap rather than assumed;
- the plugin home was marked "parked, not blocking" while a Done-when
  criterion depended on it. It is now marked blocking, and **grove** — the
  candidate the standing corpus nominates and the earlier draft omitted —
  is named;
- the id is now **confirmed** free: `kodhama/kodhama` holds only `0009`.
  `0024` is also free and unexplained by any record; minting `0026` leaves
  that hole unaccounted for, which is a known and accepted cost;
- `status` moved `draft` → `gated`, and `(DRAFT)` is out of the title. An
  approved record in this corpus has carried `(DRAFT)` in its H1 since
  2026-07-12 because append-only would not let anyone remove it;
- the "triple-encoded" claim in the Why was factually wrong and is corrected
  above, with the measurement that replaced it;
- routing and provenance, two of the eight indicted dimensions, were
  dispositioned only in a mutable file. Decision 6 now closes them here.

**The taxonomy this record ratifies has NOT passed its own review.** The
spec-adversary returned `NEEDS-REVISION` with eight blocking findings against
`SKILL.md` and `reference/taxonomy.md` — undecidable classifications, two
internal contradictions, and a stage vocabulary undefined for three of six
types. Those are unrepaired at the time of writing. **This record should not
be ratified ahead of them**, since Decision 2's "closed vocabulary" is the
thing under indictment.

**Not independently re-reviewed.** The reviews above bind to `90a7bbb`; this
revision is a new state and owes a fresh pass. The author did not grade its
own decision and did not open the intent gate.
