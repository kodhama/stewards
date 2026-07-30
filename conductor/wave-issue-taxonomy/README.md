# Staging — issue taxonomy wave

**Nothing here is in its final home.** These are the wave's working drafts,
parked under `conductor/` because that is where cross-repo wave material
lives in this repo, and because two of them are destined for repositories
this branch cannot place them in.

Kept here so they stop living in volatile temp. Each relocates when its lane
resolves — see [`../wave-issue-taxonomy.md`](../wave-issue-taxonomy.md).

| File | Final home | Blocked on |
|------|-----------|------------|
| `decision-0026-draft.md` | `kodhama/kodhama` → `decisions/0026-issue-taxonomy.md` | Lane A — independent review, then the maintainer's intent act. Confirm `0026` is free first: `0024` is cited by `wave-family-consolidation.md` but was never created |
| `plugin/skills/issues/**` | the plugin that carries the taxonomy | Lane B — **plugin home unresolved.** The Stewards `kodhama` plugin is scoped to CI marketplace setup and widening it contradicts that narrowness; its own repo on the grove/trellis/wisp `git-subdir` pattern is the consistent alternative |
| `plugin/scripts/seed-issue-taxonomy.sh` | same plugin, **outside** `skills/` | Lane B. Deliberately not inside the skill: bundling an actuator into reference content is what forced guardrails into the first draft |
| `plugin/migration/legacy-mapping.md` | rides the ratified decision, not the plugin | Lane A. Deliberately out of standing agent context — a mapping table plus counts reads as a backlog-sweep plan |

## Status

- **The taxonomy is drafted and internally consistent.** The seed script
  dry-runs clean and deletes nothing.
- **Not independently reviewed.** The same author drafted the taxonomy, the
  decision, and this staging note. Review is owed before the intent act.
- **Two vocabulary questions were settled against the corpus**, not by
  preference — no `Idea` type, and `consider` ≡ `idea` ≡ `stage: triage`.
  The evidence is in `plugin/skills/issues/reference/taxonomy.md` §5.
- **Nothing here authorises a change to any repository**: no label creation,
  no issue migration, no plugin enablement. Those are the wave's lanes, and
  the wave is not open.
