# Legacy mapping — one-time migration reference

**Not part of the skill.** This is a one-off exercise that rides with the
ratifying decision. It is kept out of standing agent context deliberately: a
mapping table plus occurrence counts reads as a backlog-sweep plan, and no
agent should be handed one as ambient context.

Nothing here authorises an edit. Migrating existing issues is a separate,
explicitly approved action.

Source: scan of all ten kodhama repos, July 2026. Counts are observed
occurrences across all repos.

---

## Title prefixes → structured metadata

| Legacy | Count | Becomes |
|--------|-------|---------|
| `[bug]` | 24 | type `Bug` |
| `[idea]` | 19 | `stage: triage` + the type its content implies |
| `[shaping]` | 19 | `stage: shaping` |
| `[execution]` | 18 | `stage: active` |
| `[consider]` | 14 | `stage: triage` + the type its content implies |
| `[high-priority]` / `HIGH:` | 12 | `priority: p1` |
| `[Story]` | 11 | type `Feature`, as a sub-issue of its epic |
| `[chore]` | 10 | type `Task` |
| `[meta]` | 9 | `area: meta` |
| `[divergent-research]` | 8 | type `Research` + `stage: shaping` |
| `[Epic]` | 6 | type `Epic`, with real sub-issues attached |
| `[design-upstream]` | 6 | **per-issue judgment — see below** |
| `idea:` | 5 | `stage: triage` + the type its content implies |
| `Tutoring:` `Morph:` `Riders:` `Settings:` `b3:` | 5 | `area: *`, repo-local — these were areas all along |
| `[kit]` `[gate]` `[durability]` `[adjudicate]` | 4 | `area: *`, repo-local to sdd-gauntlet |
| `[experiment]` | 3 | type `Research` |
| `[stage-0]` `[stage-1]` `[stage-2]` | 3 | `area: <phase>` — **not** grove stages; see judgment calls |
| `cleanup:` `test:` `review-bookkeeping:` | 3 | type `Task` |
| `[feature]` | 2 | type `Feature` |
| `[design-feedback]` | 2 | `area: design` |
| `Decide:` | 2 | type `Decision` |
| `[validation]` | 1 | `stage: review` |
| `[discovery]` | 1 | type `Research` + `stage: shaping` |
| `[papercut]` | 1 | type `Bug` + `priority: p2` |
| `[maintainer-action]` | 1 | `needs-human` |
| `[user-feedback]` | 1 | `area: <feature>` + note the source in the body |
| `[program]` | 1 | type `Epic` |
| `[product]` | 1 | `area: product` |
| `[rollout]` | 1 | type `Task` |
| `[deferred]` | 1 | `deferred` |
| `[corpus-reviewer]` | 1 | `area: corpus-reviewer` |
| `[study]` | 1 | type `Research` |
| `Plan:` | 1 | type `Task` |
| `experiment:` | 1 | type `Research` |
| `README.md:` | 1 | `area: docs` |
| *(no prefix)* | ~95 | type required; everything else as it applies |

## Existing labels → structured metadata

| Legacy label | Uses | Becomes |
|--------------|------|---------|
| `roadmap` | 45 | **Deferred — keep untouched.** See taxonomy §6 |
| `idea` | 12+ | `stage: triage` |
| `bug` (stock) | 11 | type `Bug` |
| `chore` | 10 | type `Task` |
| `priority: low` | 6 | `priority: p2` |
| `design-upstream` | 6 | **per-issue judgment — see below** |
| `meta` | 4 | `area: meta` |
| `enhancement` (stock) | 4 | type `Feature` |
| `agent-task` | 3 | `stage: ready` |
| `priority: high` | 2 | `priority: p1` |
| `priority: medium` | 1 | *(unset — normal is the default)* |
| `program` | 1 | type `Epic` |
| `design-feedback` | 1 | `area: design` |
| `shaping` | — | `stage: shaping` |
| `consider` | — | `stage: triage` |
| `documentation` (stock) | — | `area: docs` |
| `question` (stock) | — | type `Research` |
| `duplicate` `invalid` `wontfix` (stock) | — | close with `--reason not-planned` |
| `good first issue` `help wanted` (stock) | — | **keep**. GitHub surfaces these natively to outside contributors, and six of these repos are public |

## Judgment calls in the mapping

Flagged so they can be overturned rather than inherited silently.

- **`[consider]` and `[idea]` both become `stage: triage`, not a type.**
  Settled against the corpus — see `reference/taxonomy.md` §5. In short: they
  are repo dialect for the same thing (grove says one, math-quest the other,
  with indistinguishable outcomes), they span every kind of work, and 10 of
  the 38 closed as COMPLETED. A label that dissolves when work finishes is a
  lifecycle position, not a kind. **Each such issue needs its real type
  assigned during migration** — that is the bulk of the work here.
- **`[design-upstream]` (6) cannot be mapped mechanically.** In its origin
  repo the label is documented as "findings queued FOR the design side" — the
  repo *asking* design a question. `needs-design-system` means the opposite:
  this issue is *waiting on* a design-system change. Same label, two
  directions. Each of the six needs reading: a question for design becomes an
  issue filed in design-system; only a genuine wait becomes
  `needs-design-system`.
- **`[user-feedback]` and `[design-feedback]` lose their provenance
  dimension.** Three occurrences did not justify a ninth dimension, so the
  source moves into the issue body. If it must be filterable, add `from: user`.
- **`[papercut]` becomes `Bug` + `priority: p2`** rather than its own type.
  It describes size and annoyance, not kind.
- **`[stage-0/1/2]` in sdd-gauntlet are deliberately NOT mapped to
  `stage: *`.** They are that experiment's protocol phases and collide by
  name only. Mapping them would be a false cognate.
- **`priority: medium` (1 use) maps to unset.** If "medium" was meaningful
  rather than a default, this loses information.

## Sequencing, if migration is approved

1. Confirm the `stage: triage` reading holds for your own issues — the
   settled analysis is in `reference/taxonomy.md` §5.
2. Seed types and labels (`scripts/seed-issue-taxonomy.sh --apply`).
3. Migrate issues repo by repo, largest first (`math-quest`, then `grove`).
4. Only once a superseded label reaches zero uses, delete it.
5. `roadmap` last, and only after the taxonomy is ratified.
