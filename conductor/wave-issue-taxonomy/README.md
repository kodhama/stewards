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
| `plugin/skills/issues/**` | the `kodhama` plugin in Stewards — **home resolved 2026-07-31** | a review pass on the current state |
| `plugin/scripts/seed-issue-taxonomy.sh` | same plugin, **outside** `skills/` | Deliberately not inside the skill: bundling an actuator into reference content is what forced guardrails into the first draft |
| `plugin/DIRECTION.md` | travels with the plugin | Nothing — direction, not a decision. Records the graduation path and the coming abstract/concrete split |
| `plugin/migration/legacy-mapping.md` | rides the ratified decision, not the plugin | Lane A. Deliberately out of standing agent context — a mapping table plus counts reads as a backlog-sweep plan |

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

**It owes a fifth review pass.** Nothing here has been reviewed as it stands.

**Four factual errors in the author's own evidence, all caught by review:**

- a claim that a repo triple-encoded kind including a native type — wrong;
- its replacement, "0 of 465", counted pull requests — also wrong;
- `depends_on` used bare cross-repo ids on one record's practice, which the
  author then called "a defect by the declared grammar" — an over-read: the
  companions say such referents are *permitted*, not mandated, and state no
  grammar for `depends_on` at all. Both claims are withdrawn;
- an edit deleted a sentence's predicate and left the subject, shipping an
  unreadable clause.

**Nothing here authorises a change to any repository**: no label creation, no
issue migration, no plugin enablement. Those are the wave's lanes, and the
wave is not open.
