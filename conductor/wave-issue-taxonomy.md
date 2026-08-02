# Wave: issue taxonomy rollout

> **CLOSED 2026-08-02 — archive. Nothing below is current state.**
> The ledger stopped on this date under
> [`kodhama-0027`](../decisions/0027-work-is-tracked-in-issues-not-conductor-briefs.md)
> D5 (*"existing briefs become archive, not debt… they stop being updated"*).
> Current state lives in
> [stewards#79](https://github.com/kodhama/stewards/issues/79). **The lane
> boxes below are wrong in both directions** — see §Report for what actually
> landed and where the rest went.

Drafted 2026-07-30. **Authority: `kodhama-0026-issue-taxonomy`,
ratified by the maintainer's intent act on 2026-07-31** — *"I approve, flip
it, just need to check the PR though"* — recorded by an in-PR status flip. The
agent did not open the gate.

Working drafts are staged in
[`wave-issue-taxonomy/`](wave-issue-taxonomy/README.md) — the decision text,
the taxonomy skill, the seed script, and the migration mapping. None is in
its final home; that table says where each one goes and what blocks it.

Authority (pending): `kodhama-0026-issue-taxonomy`, propagated to plugin
repositories under
[`kodhama-0022-propagate-collective-strategy`](../decisions/0022-propagate-collective-strategy.md)
and delivered under
[`kodhama-0008-family-inheritance-restate-nothing`](../decisions/0008-family-inheritance-restate-nothing.md)
§4 ("repos restate nothing").

## Scope

Two carriers, deliberately different, because 0022's scope is plugins:

**Cross-link ADRs** — the four repositories carrying a marketplace plugin
(source: `.claude-plugin/marketplace.json`):

- Grove; Trellis; Wisp; **Stewards**.

Stewards *is* a downstream target here, unlike the 0023 receipts wave: the
upstream decision lives in `kodhama/kodhama`, not in Stewards.

**Ordinary product ownership** — repositories that receive the taxonomy but
are not plugin repositories, and so take an issue rather than an ADR:

- math-quest; design-system; sdd-gauntlet; homebrew-tap; kodhama.

**Enablement** — **each repository's own act, not this wave's.** Approved
`kodhama-0021` reserves adoption to each product, and `kodhama-0026`
Decision 11 disclaims enabling anything anywhere. This wave publishes and
propagates; it does not enable. Retired Spore is not a target.

## Boundaries

- Each cross-link ADR links `kodhama-0026` and `kodhama-0022` and states only
  local applicability or follow-up. **No receipt repeats the taxonomy** — no
  dimension tables, no vocabularies, no rationale, no README index. That is
  `kodhama-0008` §4; bare pointers to the plugin-carried source are fine.
- No receipt authorizes migration of existing issues, label deletion, or
  adoption-posture change.
- **Migration of legacy issues is NOT in this wave.** The mapping exists
  (`migration/legacy-mapping.md`) and is unauthorized. It needs its own
  authority, and its real cost is that ~38 `[idea]`/`[consider]` issues each
  need a type assigned by judgment, not a mechanical swap.
- `roadmap` (45 uses, math-quest only) is untouched — a named exemption
  recorded in the taxonomy, revisited only after this wave closes.

## Ledger

**Lane A — decision (kodhama/kodhama)**
- [x] Id confirmed free (2026-07-31): `kodhama/kodhama` holds only `0009`;
      Stewards holds 0001–0023 + 0025. `0024` is free and **explained** —
      `wave-family-consolidation.md` records it was reclassified to
      `research/family-audit-2026-07.md`; there is no unaccounted hole
- [x] `kodhama-0026` independently reviewed, four rounds — every one returned
      **NEEDS-REVISION** (twelve verdict records on stewards#64, binding
      `90a7bbb`, `ff1e47c`, `7c0c54d`, `228e7ed`). Round 1's F1 was a real
      conflict with approved `kodhama-0021`, now closed
- [x] Maintainer direction on F1 (2026-07-31): resolve the `kodhama-0021`
      conflict by narrowing rather than superseding. Applied — and the
      Done-when was subsequently **emptied of delivery criteria altogether**,
      which resolves it more completely than the direction asked. Delivery
      lives in these lanes. `kodhama-0021` is a declared dependency
- [ ] Fifth review pass — the four prior rounds bind to superseded commits
- [x] **Decision ratified by maintainer intent act, 2026-07-31**
- [ ] Relocate the record to `kodhama/kodhama/decisions/0026-issue-taxonomy.md`,
      recomputing the `depends_on` prefixes for that repo (open question 3)

**Lane B — plugin home + publication**
- [x] **Plugin home settled for now (maintainer direction, 2026-07-31): the
      `kodhama` plugin in Stewards, as a staging area.** Deliberately a
      parking spot — **what the `kodhama` plugin is for stays undecided**, and
      staging this skill there defers that question rather than answering it.
      **Staging touched no scope claim; publication amends the statements that
      describe it** — see the two rulings below, and note that this line
      previously asserted the claims were untouched, which publication makes
      false. **grove was rejected on grove's own structure**: its adapter axis
      is host (`claude`/`codex`) not tracker, none of its thirteen roles is a
      product owner, and only two of its fourteen charters mention GitHub —
      hosting this would invent a tracker axis for an absent role. Graduation
      path and the abstract/concrete split are recorded in `DIRECTION.md`,
      which ships with the plugin — staged at
      `wave-issue-taxonomy/plugin/DIRECTION.md`, published to
      `plugins/kodhama/DIRECTION.md` by spec 0005
- [ ] Open, unscheduled: decide what the `kodhama` plugin is for. This skill
      stays or moves on that answer
- [x] **Maintainer ruling, 2026-07-31 — amend the standing scope claims.**
      Publication falsifies statements that the plugin's scope is narrow, so
      those statements are authorised for edit: the `distribution-scope` block
      hand-mirrored in `CLAUDE.md`, `README.md` and canonically
      `distribution/repository-scope.md`, plus `plugins/kodhama/README.md`'s
      *"It edits workflow configuration and nothing else"*, **which ships to
      consumers**. **The wording must not assert a purpose for the plugin** —
      it acknowledges skills staged there while their home is decided, nothing
      more. Review of the resulting contract found **four** further carriers,
      in scope under the same ruling: `wave-issue-taxonomy/plugin/DIRECTION.md`
      §45–47, the Lane B line above, `CLAUDE.md`'s *"and on nothing else"*, and
      **`plugins/kodhama/README.md` line 22's singular *"the declared skill"***
      — which also ships to consumers, and which the first count missed.
      Contract and pinned wording:
      `specs/0005-issue-taxonomy-skill-publication.md` §Standing scope claims
- [x] **Maintainer ruling, 2026-07-31 — close the CI blind spot, narrowly.**
      Add `conductor/wave-issue-taxonomy/plugin/**` to the `paths:` filter in
      `.github/workflows/validate-marketplace-setup.yml`, and nothing wider.
      **The property protected is that the *test gate* — suite, validator, the
      `npm install` of two CLIs, the admission check — does not run on a
      docs-only PR.** An earlier wording of this line said such a PR gets *no
      check at all*; that is false and was false before this wave, since
      `agent-workflow-parity.yml` and `claude-code-review.yml` carry no
      `paths:` filter and run on every PR. The ruling is about cost, and stands.
      Contract: spec 0005 §Closing the CI blind spot
- [x] Plugin published to the `kodhama` marketplace, per spec 0005.
      **Merged 2026-08-01 as `5f3267c` (#64, squashed).** Verified on `main`
      rather than from the merge output: the package is exactly spec 0005 S1's
      nine paths, the actuator kept mode `100755` through the squash, only
      `migration/` remains under the staging directory as S6 requires, and the
      gate is green — 28 tests, validator passed. Spec 0005 merged at
      `status: approved`, flipped on the maintainer's in-session act and left
      at v9 so `tests/TEST_DEPS.md`'s `@v9` pin stays valid. **This tick is
      publication, never enablement** — `kodhama-0021` still reserves adoption
      to each repository, and Lane D remains open.
      *Superseded planning note, kept for the record:* The
      payload sits at `plugins/kodhama/` with `VERSION` at `0.3.0`, both
      manifests and both catalog descriptions updated, and the four staged
      files relocated. Conformance returned **PASS** — `SKILL.md` and
      `reference/taxonomy.md` are the identical git blobs as their staged
      predecessors, literal **G** is byte-identical, literal **H** landed at
      line 39 as spec 0005 v8 predicted, and twenty independent mutations were
      caught. Code review returned one HIGH — **the actuator's dry-run default
      was asserted in six pinned literals and guarded by nothing**; spec 0005
      v9 adds S17/R19 to close it. Left unchecked deliberately: nothing is
      published until #64 merges, and `kodhama-0021` still reserves adoption to
      each repository, so this tick is publication, never enablement

**Lane C — cross-link ADRs** *(one PR per repo, independently reviewed)*
- [ ] Grove
- [ ] Trellis
- [ ] Wisp
- [ ] Stewards

**Lane D — enablement** *(the delivery that actually reaches cloud sessions)*
- [ ] **Each repo decides for itself; this lane records opt-ins rather than
      performing them.** A repo that opts in lists the plugin under
      `enabledPlugins`. **Declaring the marketplace is not enough** — plugins
      enabled only in user settings do not transfer to cloud sessions or
      routines. *(Corrected 2026-08-01: this line said Stewards carries
      `"enabledPlugins": {}`. It has carried `grove@kodhama` and
      `trellis@kodhama` for some time; the claim was stale, not load-bearing.)*
- [x] **Stewards — opted in 2026-08-01.** `"kodhama@kodhama": true` added to
      `.claude/settings.json`. **Authority is `kodhama-0021`'s standing
      permission, not a new decision**: *"Stewards may cross-dogfood relevant
      family plugins during ordinary development."* Posture is `dogfood` per
      `kodhama-0021` Decision 1 — no support claim, breakage absorbed
- [ ] Grove, Trellis, Wisp, design-system — each may opt in on the same
      standing permission, in its own PR. **Deliberately not done in one
      sweep:** `kodhama-0021` §4 requires *"one bounded step plus a
      stop-and-learn checkpoint rather than a whole-family wave"*, and Stewards
      is that bounded step. Revisit once the skill has been observed firing
      here on real issue work
- [ ] math-quest — **a distinct act with a distinct posture, not part of the
      above.** `kodhama-0021` §3: *"Math Quest is a tree and therefore a
      preview candidate, not a steward dogfooding environment. Its
      personal-project status does not erase the distinction."* Needs its
      maintainer's explicit opt-in under `preview`
- [ ] sdd-gauntlet, kodhama — **unclassified.** Neither is recorded as steward
      or tree anywhere in this repository, and posture follows class. Classify
      before enabling either
- [ ] homebrew-tap — excluded while it carries no issues, on the same ground
      the seeding actuator skipped it

**Recorded 2026-08-01, so it is not rediscovered.** A draft `kodhama-0027`
proposed discharging `kodhama-0021` AC7's collective-rollout hold to enable
everywhere at once. **Independent review returned UNSOUND and it was deleted.**
Its ground was `kodhama-0026` Decision 11's *"binds the whole forest, trees
included"* — quoted four words short of *"**The plugin does not.**"*, which is
the same clause deciding the opposite. Decision 9 also defeats the draft's
second premise: the convention *"is operable the moment"* the types and labels
exist, so it is already in force and readable; what the plugin adds is
teaching. **And the instrument was inverted** — every repo it could lawfully
reach was already permitted by `kodhama-0021`, so its only new authority ran
over the repos that decision most protects. No decision is needed for the
steward opt-ins; one would be needed to reach math-quest, and it would have to
argue the teaching gap honestly rather than claim an incoherence.

**Lane E — provisioning**
- [x] `gh auth refresh -h github.com -s admin:org` — run by the maintainer
      2026-07-31; the token now carries `admin:org`, `gist`, `repo`, `workflow`
      (`read:org` is subsumed). The actuator's own preflight named the missing
      scope and printed this command
- [x] Org issue types created: `Research`, `Decision`, `Epic` — seeded
      2026-07-31 with `--types-only --apply`, exit 0. **Verified against the
      API rather than the script's output**: `/orgs/kodhama/issue-types`
      returns six types, all `is_enabled: true` — the three new ones plus the
      pre-existing `Task`, `Bug`, `Feature`, which were left untouched
- [x] Labels seeded per repo — run 2026-08-01 with `--labels-only --apply`
      after #64 merged, so the skill explaining the vocabulary arrived first.
      **120 labels across 8 repos, verified against the labels API rather than
      the script's own ✓ output: 15/15 in each of trellis, grove, wisp,
      math-quest, design-system, kodhama, stewards and sdd-gauntlet.**
      `homebrew-tap` skipped on the empty-backlog gate — 0/15, as intended;
      `--force` would seed it. No label was deleted and no issue was touched.
      The redundant stock labels (`bug`, `enhancement`, `idea`, …) are reported
      and left in place: migrating the issues carrying them is a separate act
      this wave does not authorise

**Note on order.** The vocabulary now exists org-wide while nothing consumes
it: the skill reaches repos only once #64 merges and the plugin is installed.
That gap is deliberate — types are the reversible half — but it means the
convention is **not** in force yet, whatever the org API now reports.

**Lane F — math-quest**
- [ ] Receiving issue filed in math-quest (product ownership, not a
      cross-link ADR — see Scope)
- [ ] **Rider: pay the `wave-0008-rollout` debt.** That wave recorded
      math-quest's stale lifecycle copy as "math-quest's own issue — **not
      yet filed**", blocked 2026-07-12 by a same-owner platform restriction
      ("gundisalwa-tier repo, kodhama-tier session"). **That blocker is
      gone**: math-quest is `owner: kodhama (Organization)` as of this check.
      The debt is payable and should ride this lane

## Parked

1. **`roadmap` → GitHub Projects.** Not a taxonomy dimension; it is a
   selection. Gate: this wave closed. One reason to wait has already been
   discharged — the `stage:`-versus-Projects-Status collision is now settled
   in favour of the label, because agents query issues and labels travel
   while project fields do not.
2. **Priority → GitHub Issue Fields**, when Fields leaves public preview.
   Supersede `kodhama-0026`, do not edit it.
3. **Migration of legacy issues**, per Boundaries.
4. **Whether `kodhama-0017` gets a forward pointer for its AC3 scope
   enumeration.** Publishing the issue skill makes this repository's
   `distribution-scope` block describe different contents from the ones
   `kodhama-0017` AC3 records — it **adds** the skill and the actuator, and
   **removes** the marketplace-metadata description, since `kodhama-0025` §4
   redirected that goal to the GitHub Actions run log. AC3 is a frozen record
   rather than a statement of present state, so **nothing is owed as an edit**;
   what is missing is disclosure at the record. **This parks against standing
   practice**, which is why it needs an answer: in every corpus instance the
   falsifying change writes the pointer in the same change (`kodhama-0025` →
   `0017:15-18`; `-0003` → `0002:33`; `-0006` → `0002:41`), and
   `decisions/0025:151-153` budgets for exactly that. The distinction that may
   justify parking: every precedent is a *decision* annotating a decision, and
   this is a **spec**. Full reasoning in
   `specs/0005-issue-taxonomy-skill-publication.md` open question 6.

**Batch discipline (`CLAUDE.md`, ≤3 at a time).** Only item 4 is asking for a
decision now; 1–3 are gated on later events (this wave closing, Issue Fields
GA, a separate migration authority) and are not in the current batch. Spec
0005's other five open questions are deliberately **not** parked here — none
carries a live decision, and batching them would spend the cap on questions
nobody needs answered yet. That they have no ledger entry is a pre-existing
gap, recorded here rather than fixed.

## Report

Written 2026-08-02, from live `gh` and file state. This is the closure
report `kodhama-0027` D3 permits a brief to hold. **It is the last thing
written here.**

### What the wave delivered

- **`kodhama-0026` ratified** by maintainer intent act 2026-07-31, after four
  independent review rounds that all returned `NEEDS-REVISION`. It now lives
  at `kodhama/kodhama` `decisions/0026-issue-taxonomy.md` — byte-identical,
  because it is approved and append-only.
- **`specs/0005` approved at v9** and the `issues` skill plus the seeding
  actuator published in the `kodhama` plugin.
- **Provisioning**: six org issue types enabled; **120 labels, 15/15 in each of
  eight repositories.** `homebrew-tap` is the exception — 0/15, skipped by the
  actuator's empty-backlog gate, as Lane E records.
- **Enablement**: the plugin is enabled in six repositories — five stewards
  under `dogfood` and math-quest under `preview`.
- **Migration**, authorised in session after this brief was written and
  therefore outside its Boundaries: of 144 open issues across grove,
  math-quest, stewards, trellis and wisp, **all but one carry a type.** The
  exception is deliberate — kodhama/math-quest#270, the `[program]` shape #75
  records. design-system has no issues.
- **`kodhama-0027`** — written mid-wave, on evidence this wave produced: work
  is tracked in issues, and the brief stops being a ledger. It is why this
  section closes the file.

### The lane boxes are wrong in both directions

Recorded plainly, because it is the finding that justified `kodhama-0027`.

**Unticked but done.** Lane D's five eligible opt-ins — Grove, Trellis, Wisp,
design-system and math-quest, all on 2026-08-01. Lane A's relocation, done
2026-08-02. **Not all of Lane D**: its `sdd-gauntlet`/`kodhama` and
`homebrew-tap` rows are genuinely open, and are #77 below.

**Ticked but incomplete** — none found.

**Unticked and dead.** Lane A's *"fifth review pass"*: it bound to superseded
commits, and the maintainer ratified without it.

**Unticked and genuinely open — now issues, since this file can no longer
hold them:**

| Was | Now |
|---|---|
| Lane C — four cross-link ADRs; Lane F — math-quest's receiving issue | **#83** (a `Decision`: enablement and migration may have overtaken them) |
| Lane F rider — the `wave-0008-rollout` debt | **kodhama/math-quest#391** |
| Parked 2 — priority → GitHub Issue Fields | **#85** (`deferred`) |
| Parked 4 — `kodhama-0017`'s AC3 forward pointer | **#84** |
| Lane B — what the `kodhama` plugin is for | **#70** |
| Lane D — sdd-gauntlet, kodhama, homebrew-tap have no posture | **#77** |
| Parked 1 — `roadmap` → Projects, gated on *"this wave closed"* | **kodhama/math-quest#390**; this closure discharges the gate |
| Parked 3 — migration of legacy issues | done |

Consequences the wave surfaced are also issues: **#75** (two shapes the
vocabulary does not decide), **kodhama/grove#201** (everything landed at
`stage: triage`), **#72** (where lessons live), **#73**, **#65**.

All of the above hang off **stewards#79**.

### Why it closes without every lane ticked

Because the ticking is the defect. This wave produced the evidence for
`kodhama-0027`: a brief that lists work is a brief that will be wrong, and
this one was wrong in both directions within a day of its last edit. Closing
it with lanes outstanding — each one an issue that updates as a side effect
of the work — is the point, not a compromise.
