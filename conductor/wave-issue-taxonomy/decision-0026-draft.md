---
id: kodhama-0026-issue-taxonomy
type: decision
status: draft  # DRAFT — the maintainer's approval (the intent act) is pending; the intent gate is not opened by an agent
depends_on: [kodhama/kodhama-0009-org-topology-spirit-stewards-trees, kodhama-0008-family-inheritance-restate-nothing, kodhama-0022-propagate-collective-strategy]
owner: agent
updated: 2026-07-30
provenance: "shaped in session 2026-07-30 from a scan of all ten kodhama repos; two vocabulary questions settled against the corpus (no Idea type; consider ≡ idea ≡ stage: triage), evidenced in the plugin's reference/taxonomy.md §5. Placed at the org layer rather than the steward layer because it binds math-quest, a tree."
---

# Decision (DRAFT): one issue taxonomy for the forest — structured metadata, prose titles

## Why

Issue metadata across the ten repos has no shared shape. Seven of ten carry
GitHub's stock labels untouched; the actual signal rides a `[bracket]` prefix
in the title, which had accumulated **eight orthogonal dimensions in one
slot** (kind, workflow stage, priority, triage state, hierarchy, routing,
provenance, area) in two competing forms, with `(none)` the plurality in five
repos. math-quest additionally triple-encodes kind — title, label, and native
type.

The cost is not aesthetic. Nothing is queryable across repos, agent dispatch
has no reliable signal to read, and the same fact drifts between its copies.

## Decision

1. **Issue titles are prose.** No bracket prefixes, no `type:` prefixes.
   Every machine-readable dimension lives in structured metadata.
2. **Kind is the native GitHub issue type** — `Bug`, `Feature`, `Task`
   (org-provisioned) plus `Research`, `Decision`, `Epic`. Closed vocabulary.
3. **There is no `Idea` type.** "Idea" and "consider" name a commitment
   level, not a kind; commitment is carried by stage. Both become
   `stage: triage`.
4. **Stage, priority, status, and area are labels** with fixed namespaces —
   `stage:` (closed, ordered, one at a time), `priority:` (closed, unset =
   normal), status (closed), `area:` (**open and deliberately repo-local**).
5. **Hierarchy is native sub-issues**, not `[Epic]`/`[Story]` prefixes.
6. **Priority stays a label, not a GitHub Issue Field**, until Issue Fields
   leaves public preview. When it reaches GA this decision is superseded,
   not edited.
7. **The taxonomy arrives by plugin, and repos restate nothing**
   (`kodhama-0008` §4). No repo hand-authors a copy, an index, or a README
   section. Bare pointers to the plugin-carried source are permitted.
8. **Grove owns the mapping from `(type, stage)` to its workflow steps.** No
   issue is named after a grove step. The type says what an issue *is*; the
   stage says where it *is*.
9. **Scope is the whole forest, trees included** — math-quest is bound. It is
   reached through ordinary product ownership (an issue in math-quest), not
   through the `kodhama-0022` cross-link mechanism, which is scoped to plugin
   repositories.

## Done when

- The plugin carrying the taxonomy skill is published to the `kodhama`
  marketplace and enabled in each target repo's `.claude/settings.json`.
- Cross-link ADRs exist in the affected plugin repositories per
  `kodhama-0022`.
- math-quest carries its own receiving issue.
- The rollout brief `conductor/wave-issue-taxonomy.md` is closed with a
  report. Rollout completion is the **brief's** ledger, not this record's.

## Open questions (3 — parked, not blocking)

- **Where the plugin lives.** The `kodhama` plugin in Stewards is scoped to
  CI marketplace setup; widening it would contradict that narrowness. Its own
  repository, following the grove/trellis/wisp `git-subdir` pattern, is the
  consistent alternative. Unresolved.
- **`roadmap` (45 uses, math-quest only)** is a selection, not a dimension —
  Projects territory. Deliberately deferred so the backlog moves under one
  change at a time. Named exemption, not an oversight.
- **Whether legacy issues are migrated at all.** The mapping exists; this
  decision does not authorize the edit.

## Self-check (gate)

Two vocabulary questions were settled against the corpus rather than by
preference, and the evidence is recorded with the taxonomy (38 issues
examined; 10 of them closed COMPLETED, which is what rules out `Idea` as a
type). The `kodhama-0022` scope question was checked against 0022's own text
— it says "plugins" throughout and parks single-product communication — so
math-quest is routed by product ownership instead; this is a **carrier**
difference, not an exemption, and matches the `kodhama-0008` precedent that
math-quest's copy "is math-quest's own issue."

**Not independently reviewed.** The author drafted the taxonomy and this
record; an independent soundness review is owed before the intent act.
