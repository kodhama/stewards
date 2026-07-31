---
id: kodhama-0026-issue-taxonomy
type: decision
status: gated  # author self-check recorded; two independent review rounds returned NEEDS-REVISION (binding 90a7bbb and ff1e47c) and this revision answers the second — it is NOT itself reviewed. The maintainer's intent act remains open and is not opened by an agent
depends_on: [kodhama-0009-org-topology-spirit-stewards-trees, stewards/kodhama-0008-family-inheritance-restate-nothing, stewards/kodhama-0021-separate-adoption-posture-from-support, stewards/kodhama-0022-propagate-collective-strategy]
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
`Feature` provisioned as native issue types, and **not one issue in the org
carries a type — 0 of 294**, counted across all nine live repos on 2026-07-31
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
4. **Stage, priority, facing, status and area are labels**, and every closed
   one is enumerated here so the closure is enforceable by this record rather
   than by a file it points at:
   - `stage:` — `triage` · `shaping` · `drafting` · `ready` · `active` ·
     `review`. Ordered, mutually exclusive
   - `priority:` — `p0` · `p1` · `p2`, with **unset** meaning normal
   - status — `blocked` · `needs-human` · `needs-design-system` · `deferred`.
     Bare tokens; **status is not a namespace**
   - `area:` — **open and deliberately repo-local**, the only open vocabulary

   Which stages each type visits, and every rule for applying these, is the
   plugin's to state. **Membership is this record's.**
5. **`facing: user` / `facing: system`** — a closed pair — records whether
   anyone outside the building team observes the change. It is a dimension rather than a type
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
9. **The taxonomy arrives by plugin, and repos restate nothing**
   (`kodhama-0008` §4). No repo hand-authors a copy, an index, or a README
   section. Bare pointers to the plugin-carried source are permitted.
10. **Grove owns the mapping from `(type, stage)` to its workflow steps.** No
   issue is named after a grove step. The type says what an issue *is*; the
   stage says where it *is*.
11. **The convention binds the whole forest, trees included. The plugin does
    not.** Adoption of the carrying plugin is each repository's own act, per
    approved `kodhama-0021` — *"Math Quest receives no plugin change until it
    explicitly opts into preview."* This decision makes the taxonomy
    authoritative and available; it does not enable a plugin anywhere.
    Nothing here amends or supersedes `kodhama-0021`.

    **Between ratification and provisioning the convention is decided but not
    operable.** Until an org creates `Research`, `Decision` and `Epic`, the
    skill's first instruction is to stop, so ratifying this record changes no
    repository's behaviour by itself. That is the intended order — decide,
    provision, adopt — stated here so the gate's owner is not surprised by it.

## Propagation (`kodhama-0022`)

Applicable plugin repositories, from the marketplace catalog: **Grove**,
**Trellis**, **Wisp**, and **Stewards** (which carries the `kodhama` plugin
and is downstream here because the upstream record is not its own).
Non-plugin repositories receive no cross-link ADR. math-quest is reached
through ordinary product ownership — an issue in math-quest — per
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

**1. Where the plugin lives.** Not blocking this record — it is a delivery
question, owned by the brief's Lane B. It is recorded here because Decision 9
makes the plugin the sole carrier, so the convention reaches no one until it
resolves, and because **every candidate currently conflicts with something
standing.** Three, none yet chosen:
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

**3. The cross-repo reference grammar is inconsistent, and an approved record
already calls it settled.** `kodhama-0022`'s self-check says it "uses the
settled qualified-link grammar", and `.grove/versioning.md` and
`.grove/relations.md` both declare `<repo>/<id>` as the cross-repo form. This
record's `depends_on` is qualified **for its destination** (`kodhama/kodhama`)
— `kodhama-0009` bare, the three Stewards records prefixed. Correct on
arrival, and deliberately not correct while staged here. An earlier draft used
uniform bare ids on the strength of `kodhama-0009`'s own practice; that
practice is a defect by the declared grammar, not a precedent.
`kodhama-0009` (approved, in `kodhama/kodhama`) references the Stewards
record `kodhama-0002` **bare**; Stewards' `kodhama-0022` references `0009` as
`kodhama/kodhama-0009-…`. Three of four cross-repo references in the shared
namespace are bare. This record follows the destination repository's own
A ruling would settle four existing
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

**Review history, so this state is not overstated.** Three rounds have run —
nine verdict records on stewards#64, binding `90a7bbb`, `ff1e47c` and
`7c0c54d`. **None passed.** The items below were round 1's:
- the conflict with approved `kodhama-0021` was real and uncited. Resolved by
  maintainer direction of 2026-07-31: **narrow the Done-when** to publication
  plus repo-owned opt-in, rather than supersede 0021. Decision 11 now states
  the convention/plugin split explicitly;
- the `kodhama-0022` invocation named no targets. A propagation section now
  does, and the mechanism's reach over an org-layer upstream is recorded as
  an open gap rather than assumed;
- the plugin home was marked "parked, not blocking" while a Done-when
  criterion depended on it. It is now marked blocking, and **grove** — the
  candidate the standing corpus nominates and the earlier draft omitted —
  is named;
- the id is now **confirmed** free: `kodhama/kodhama` holds only `0009`.
  `0024` is also free and **explained**: `conductor/wave-family-consolidation.md`
  records that the intended `0024` was reclassified to
  `research/family-audit-2026-07.md`, so "the ids jump 0023 → 0025". An
  earlier draft called it unexplained and accepted a cost that does not
  exist — the claim was false against a brief in the same directory;
- `status` moved `draft` → `gated`, and `(DRAFT)` is out of the title. An
  approved record in this corpus has carried `(DRAFT)` in its H1 since
  2026-07-12 because append-only would not let anyone remove it;
- the "triple-encoded" claim in the Why was factually wrong and is corrected
  above, with the measurement that replaced it;
- routing and provenance, two of the eight indicted dimensions, were
  dispositioned only in a mutable file. Decision 7 now closes them here.

**The taxonomy has been repaired twice and reviewed twice.** Round 1's eight
blocking spec findings are all addressed. Round 2 returned seven further
blocking findings against the constructs those repairs introduced — `facing:`
defined against two boundaries, `Epic` called orthogonal to a single-valued
field, an `Epic` stage rule answering one question three ways, and
`Decision`/`Research` losing their dispatch stage. This revision answers those
and reconciles the record to the spec, which is the root cause round 2 named:
the two had been repaired in separate passes and diverged for five commits.

**Not independently reviewed in this state.** The two rounds bind to
`90a7bbb` and `ff1e47c`; this is a third state and owes a fresh pass. Round 2
also found the author's own *corrected* measurement still wrong — the count
that replaced a false claim carried a denominator inflated by pull requests.
Two independent readers caught it; the author did not. The author did not
grade its own decision and did not open the intent gate.
