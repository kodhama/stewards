# Wave: adoption-posture acknowledgments

Opened 2026-07-25. Authority:
[`kodhama-0021-separate-adoption-posture-from-support`](../decisions/0021-separate-adoption-posture-from-support.md)
and the maintainer's follow-up direction to inform the family through small,
local decision PRs.

## Purpose

Give each decision-bearing member an early, durable pointer to the collective
adoption-posture model without waiting for unrelated product work to encounter
it. Each local decision imports decision 0021 rather than restating its
definitions, records only that repository's own posture choice, and changes no
support claim by implication.

This is a sequential acknowledgment wave, not an implementation wave. Only one
product lane is active at a time. Every PR is followed by a stop-and-learn
checkpoint before another lane is unlocked.

## Boundaries

- No shared registry, schema, certification process, release gate, version
  coordination, support evaluator, or rollout automation.
- No package, catalog, source, setup, surface-matrix, or release change rides
  an acknowledgment decision.
- Dogfood or preview never establishes `supported`; support evidence remains
  product- and host-owned.
- A repository that has no genuine local posture choice receives no
  performative decision merely for visibility.

## Sequence and ledger

### 1. Grove — active

- [x] Open a short Grove decision that classifies ordinary use of its
      implemented `implementation-planner` as dogfood:
      [grove PR #144](https://github.com/kodhama/grove/pull/144).
- [ ] Preserve ADR-0037's routing and transient handoff unchanged.
- [ ] Keep experiment metrics, release behavior, candidate surfaces, support
      promotion, and broader rollout parked.
- [ ] Stop and record the checkpoint before unlocking another repository.

### 2. Trellis — locked

One short decision may acknowledge decision 0021 and permit relevant steward
dogfood. It must not activate a plugin or make a support claim merely by
acknowledging the model.

### 3. Wisp — locked

One short decision may acknowledge decision 0021 and permit relevant steward
dogfood. The existing Wisp catalog candidate is outside this acknowledgment
and receives no approval from it.

### 4. Design System — locked

One short decision may acknowledge decision 0021 and permit relevant steward
dogfood. No distribution or generated-asset behavior changes by implication.

### 5. Math Quest — locked

Math Quest is a tree, so any local posture would be preview, never steward
dogfood. Its acknowledgment does not opt it in; preview requires a separate,
explicit maintainer choice and a practical rollback path.

## Deliberate exclusions

- **Stewards:** decision 0021 is already the shared authority.
- **Homebrew Tap:** delivery-only and without a decision corpus; no local
  posture choice currently justifies inventing one.
- **kodhama/kodhama:** the forest-spirit front door, not an operational
  product or steward.
- **Spore:** retired.
- **sdd-gauntlet:** topology remains unresolved.
- **demo-repository:** not part of the canonical topology.

## First checkpoint

After Grove's PR is open, record:

- whether the reference-only decision stayed short and locally meaningful;
- whether it accidentally implied release, surface, or support changes;
- whether any terminology or dependency-format problem should be corrected
  before repeating the pattern; and
- the maintainer's explicit choice to unlock or stop the next lane.

## Report

Open. Grove is the only authorized product lane. Its draft is decision-only:
ADR-0038 plus a proposed forward annotation on ADR-0037, with all generated
projections and 172 tests passing. No later lane is unlocked.
