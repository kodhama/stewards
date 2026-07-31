# Wave: issue taxonomy rollout

**OPEN.** Drafted 2026-07-30. **Authority: `kodhama-0026-issue-taxonomy`,
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
      path and the abstract/concrete split are recorded in
      `wave-issue-taxonomy/plugin/DIRECTION.md`
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
      more. Review of the resulting contract found three further carriers,
      in scope under the same ruling: `wave-issue-taxonomy/plugin/DIRECTION.md`
      §45–47, the Lane B line above, and `CLAUDE.md`'s *"and on nothing else"*.
      Contract and pinned wording:
      `specs/0005-issue-taxonomy-skill-publication.md` §Standing scope claims
- [x] **Maintainer ruling, 2026-07-31 — close the CI blind spot, narrowly.**
      Add `conductor/wave-issue-taxonomy/plugin/**` to the `paths:` filter in
      `.github/workflows/validate-marketplace-setup.yml`, and nothing wider:
      **ordinary docs PRs must still get no check**, which is the property
      `CLAUDE.md` protects. Contract: spec 0005 §Closing the CI blind spot
- [ ] Plugin published to the `kodhama` marketplace, per spec 0005

**Lane C — cross-link ADRs** *(one PR per repo, independently reviewed)*
- [ ] Grove
- [ ] Trellis
- [ ] Wisp
- [ ] Stewards

**Lane D — enablement** *(the delivery that actually reaches cloud sessions)*
- [ ] **Each repo decides for itself; this lane records opt-ins rather than
      performing them.** A repo that opts in lists the plugin under
      `enabledPlugins`. **Declaring the marketplace is not enough** —
      Stewards currently carries `"enabledPlugins": {}`, and plugins enabled
      only in user settings do not transfer to cloud sessions or routines

**Lane E — provisioning**
- [ ] `gh auth refresh -h github.com -s admin:org` — the maintainer's token
      currently has `read:org` only, so custom issue types cannot be created
- [ ] Org issue types created: `Research`, `Decision`, `Epic`
- [ ] Labels seeded per repo (`scripts/seed-issue-taxonomy.sh --apply`).
      Idempotent, deletes nothing, reports superseded labels only

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

## Report

*(appended at closure)*
