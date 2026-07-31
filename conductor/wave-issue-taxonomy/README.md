# Staging — issue taxonomy wave

**Nothing here is in its final home.** These are the wave's working drafts,
parked under `conductor/` because that is where cross-repo wave material
lives in this repo, and because two of them are destined for repositories
this branch cannot place them in.

Kept here so they stop living in volatile temp. Each relocates when its lane
resolves — see [`../wave-issue-taxonomy.md`](../wave-issue-taxonomy.md).

| File | Final home | Blocked on |
|------|-----------|------------|
| `decision-0026-issue-taxonomy.md` | `kodhama/kodhama` → `decisions/0026-issue-taxonomy.md` | Lane A — a fresh review pass on this revision, then the maintainer's intent act. **Id confirmed free** 2026-07-31: `kodhama/kodhama` holds only `0009` |
| `plugin/skills/issues/**` | the plugin that carries the taxonomy | A third review pass. Then Lane B — **plugin home unresolved (BLOCKING)**, three candidates including grove |
| `plugin/scripts/seed-issue-taxonomy.sh` | same plugin, **outside** `skills/` | Lane B. Deliberately not inside the skill: bundling an actuator into reference content is what forced guardrails into the first draft |
| `plugin/migration/legacy-mapping.md` | rides the ratified decision, not the plugin | Lane A. Deliberately out of standing agent context — a mapping table plus counts reads as a backlog-sweep plan |

## Status

**Two review rounds have run, both against superseded states. Neither
passed.** All six verdict records are on
[stewards#64](https://github.com/kodhama/stewards/pull/64).

| Round | Binds to | Outcome |
|---|---|---|
| 1 | `90a7bbb` | decision `NEEDS-REVISION` · spec `NEEDS-REVISION` (8 blocking) · corpus not sound |
| 2 | `ff1e47c` | decision `NEEDS-REVISION` · spec `NEEDS-REVISION` (7 blocking, 3 regressions) · corpus not sound |

**Round 2 named the root cause:** the record and the taxonomy had been
repaired in separate passes and diverged for five commits, so the record
ratified an artifact it no longer described. This state answers round 2 and
reconciles the two in a single pass — the record, the spec, the brief and the
seeding script all move together.

**It owes a third review pass.** Nothing here has been reviewed in its
current state.

**Three factual errors in the author's own evidence, all caught by review:**

- a claim that a repo triple-encoded kind including a native type — **wrong**;
- its replacement, "0 of 465", carried a denominator inflated by pull
  requests — **also wrong**. The correct figure is 0 of 294, org-wide;
- `depends_on` used bare cross-repo ids on the strength of one record's
  practice, which the declared grammar in `.grove/versioning.md` makes a
  defect rather than a precedent.

**Nothing here authorises a change to any repository**: no label creation, no
issue migration, no plugin enablement. Those are the wave's lanes, and the
wave is not open.
