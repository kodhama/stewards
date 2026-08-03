# Staging — issue taxonomy wave

**What remains here is not in its final home.** These are the wave's working
drafts, parked under `conductor/` because that is where cross-repo wave
material lives in this repo, and because one of them was destined for a
repository this branch could not place it in.

Kept here so they stop living in volatile temp. Each relocates when its lane
resolves — see [`../wave-issue-taxonomy.md`](../wave-issue-taxonomy.md).

**Only the migration mapping is still staged here.** The plugin files were
published per `specs/0005-issue-taxonomy-skill-publication.md`, and
`kodhama-0026` landed at the org layer. Their rows record where each one
landed rather than where it was going.

| File | Final home | Blocked on |
|------|-----------|------------|
| ~~`decision-0026-issue-taxonomy.md`~~ | **landed** in `kodhama/kodhama` at `decisions/0026-issue-taxonomy.md` (kodhama/kodhama#56) — byte-identical, because the record is approved and append-only | Nothing. **Id confirmed free** 2026-07-31: `kodhama/kodhama` held only `0009` |
| ~~`plugin/skills/issues/**`~~ | **published** to `plugins/kodhama/skills/issues/` — `SKILL.md` and `reference/taxonomy.md` | Nothing. Host skill discovery reads `<plugin>/skills/<name>/SKILL.md`, so the directory name equals the skill's `name: issues` |
| ~~`plugin/scripts/seed-issue-taxonomy.sh`~~ | **published** to `plugins/kodhama/scripts/seed-issue-taxonomy.sh` — same plugin, **outside** `skills/` | Nothing. Deliberately not inside the skill: bundling an actuator into reference content is what forced guardrails into the first draft, and everything under `skills/` is agent-reachable by construction |
| ~~`plugin/DIRECTION.md`~~ | **published** to `plugins/kodhama/DIRECTION.md`, the plugin root | Nothing — direction, not a decision. It travels with the plugin, and `reference/taxonomy.md` §6.5 points at `../../../DIRECTION.md`, which resolves there and nowhere else |
| `plugin/migration/legacy-mapping.md` | rides the ratified decision, not the plugin — so `kodhama/kodhama`, per `specs/0005` §What does not ship | **#87 — the move is owed, and asks whether the contract is right.** Lane A resolved 2026-08-02, so the spec's *"until that lane resolves"* no longer holds it here. **Deliberately not published**: out of standing agent context — a mapping table plus counts reads as a backlog-sweep plan — and it authorises nothing, since `kodhama-0026` open question 5 leaves migration unauthorised |

## Status

**Four review rounds have run, each against a state now superseded. None
passed.** All twelve verdict records are on
[stewards#64](https://github.com/kodhama/stewards/pull/64).

| Round | Binds to | Outcome |
|---|---|---|
| 1 | `90a7bbb` | decision + spec `NEEDS-REVISION` (8 blocking) · corpus not sound |
| 2 | `ff1e47c` | decision + spec `NEEDS-REVISION` (7 blocking, 3 regressions) · corpus not sound |
| 3 | `7c0c54d` | decision + spec `NEEDS-REVISION` (6 blocking) · corpus not sound |
| 4 | `228e7ed` | decision + spec `NEEDS-REVISION` (6 blocking) · corpus not sound |

**The recurring failure is a process one, named by round 4's spec reviewer:**
repairs are made at the point of the reported defect, and the passages that
*depend on* the repaired text are not re-walked. This state was produced with
the check it proposed — for each construct changed, grep every occurrence of
its key terms and re-read each hit.

**Ratified 2026-07-31** by the maintainer's intent act, recorded as an in-PR
status flip. Round 5 added the first conformance review (**fidelity PASS both
directions**) and a practitioner review (**"ship it"**); their four blockers
were cleared in `191b7c5`.

**In force since 2026-08-01 in eight repositories**, on the stricter of two
criteria that disagree. `kodhama-0026` Decision 9 makes the convention operable
*"the moment"* the org issue types **and** the labels exist: types were seeded
2026-07-31, labels 2026-08-01, so 08-01 is the date — and because labels are
per-repository, so is the date. **`homebrew-tap` is the exception**, at 0 of 15
labels, skipped by the actuator's empty-backlog gate.

`SKILL.md`'s own gate checks **only** the six issue types, so it would report
the convention in force there anyway. That divergence is #107.

**Four factual errors in the author's own evidence, all caught by review:**

- a claim that a repo triple-encoded kind including a native type — wrong;
- its replacement, "0 of 465", counted pull requests — also wrong;
- `depends_on` used bare cross-repo ids on one record's practice, which the
  author then called "a defect by the declared grammar" — an over-read: the
  companions say such referents are *permitted*, not mandated, and state no
  grammar for `depends_on` at all. Both claims are withdrawn;
- an edit deleted a sentence's predicate and left the subject, shipping an
  unreadable clause.

**Nothing here authorised a change to any repository**: no label creation, no
issue migration, no plugin enablement. Those were the wave's lanes, and all
three were later authorised separately — provisioning on 2026-07-31, migration
and enablement in session on 2026-08-01. The wave closed as archive on
2026-08-02; this sentence describes what this staging directory conferred, not
the state of the family.
