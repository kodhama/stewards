# Bounded step: Trellis Codex preview catalog admission

Opened 2026-07-26. Authorities:

- Stewards
  [`kodhama-0021-separate-adoption-posture-from-support`](../decisions/0021-separate-adoption-posture-from-support.md);
  and
- Trellis
  [`decision-0063-permit-codex-preview-adoption`](https://github.com/kodhama/trellis/blob/main/decisions/0063-permit-codex-preview-adoption.md),
  approved and merged through
  [Trellis PR #194](https://github.com/kodhama/trellis/pull/194).

## One bounded step

Add Trellis to the Stewards Codex catalog as an opt-in preview:

- point only to the product-owned `kodhama/trellis/plugins/trellis` package;
- state that the catalog listing makes no support claim;
- preserve the existing Claude catalog entry unchanged; and
- add the smallest exact-shape regression test for the entry.

The implementation is
[Stewards PR #40](https://github.com/kodhama/stewards/pull/40).

## Boundaries

- No Trellis package, version, setup, hook, surface metadata, or support claim
  changes.
- No Claude catalog or delivery change.
- No family-wide rollout, maturity model, catalog schema, or automation.
- No hosted Trellis behavior test. Trellis issue
  [#182](https://github.com/kodhama/trellis/issues/182) remains parked for
  exact GitHub Actions behavior and support evidence.
- No Codex lifecycle or cloud promotion.

## Ledger

- [x] Trellis product decision approved and merged.
- [x] Stewards catalog PR opened and linked.
- [x] Red control proved the regression test fails without the entry.
- [x] Full Stewards tests and repository validation passed.
- [x] Claude, Codex, mixed, and repository-validation hosted jobs passed.
- [x] An isolated Codex home registered the changed catalog and installed
      `trellis@kodhama` version `0.2.0`; no model was started.
- [x] Independent reviews ran and their test-dependency, coordination, and
      duplicate-row findings were incorporated.
- [ ] PR #40 merge. Its merge closes this brief without starting another
      product or family lane.

## Stop-and-learn checkpoint

The bounded acquisition question is answered: the source pointer resolves to
the product-owned Trellis 0.2.0 package, its Codex manifest and hook descriptor
are present after installation, and catalog registration still works in the
separate Claude, Codex, and mixed hosted jobs.

That evidence proves acquisition only. It does not prove model-visible rule
delivery, exactly-once behavior, live-row reload, fallback behavior, GitHub
Actions support, or cloud support.

**Recommendation:** after fresh review of the repaired final diff, merge PR
#40 and stop. Do not dispatch Trellis issue #182 or any wider rollout from this
brief.
