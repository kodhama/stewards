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
| `plugin/skills/issues/**` | the plugin that carries the taxonomy | **Eight blocking spec-adversary findings, unrepaired.** Then Lane B — plugin home unresolved, now with grove as a third candidate |
| `plugin/scripts/seed-issue-taxonomy.sh` | same plugin, **outside** `skills/` | Lane B. Deliberately not inside the skill: bundling an actuator into reference content is what forced guardrails into the first draft |
| `plugin/migration/legacy-mapping.md` | rides the ratified decision, not the plugin | Lane A. Deliberately out of standing agent context — a mapping table plus counts reads as a backlog-sweep plan |

## Status

**Three independent reviews returned 2026-07-31, all posted to
[stewards#64](https://github.com/kodhama/stewards/pull/64) against commit
`90a7bbb`. None passed.**

| Reviewer | Verdict |
|---|---|
| `grove:decision-adversary` | `NEEDS-REVISION` — 3 load-bearing, 7 repairable |
| `grove:spec-adversary` | `NEEDS-REVISION` — 8 blocking, 8 non-blocking |
| `grove:corpus-reviewer` | corpus not sound — 1 hard FAIL, 8 dangling refs, all pre-existing |

**The decision record has been revised** against the decision-adversary and
corpus-reviewer findings, and against the maintainer's direction of
2026-07-31 to narrow the Done-when rather than supersede `kodhama-0021`. It
owes a fresh review pass: the verdicts above bind to `90a7bbb`, and this is a
new state.

**The taxonomy itself is unrepaired.** The spec-adversary's eight blocking
findings — two internal contradictions, a stage vocabulary undefined for
three of six types, no tie-break for multi-matching types, a dead relative
path, and three type names that do not exist in the org — all stand. The
decision should not be ratified ahead of them, since the vocabulary it
declares closed is the thing under indictment.

**Two factual corrections were forced by review**, both in the author's own
evidence:

- the claim that math-quest triple-encodes kind including a native type was
  **wrong**. Zero of 465 issues sampled across six repos carry any native
  type. The types are provisioned, never applied;
- the repo denominator counted retired Spore. Six of nine live repos carry
  stock labels, not seven of ten.

**Nothing here authorises a change to any repository**: no label creation, no
issue migration, no plugin enablement. Those are the wave's lanes, and the
wave is not open.
