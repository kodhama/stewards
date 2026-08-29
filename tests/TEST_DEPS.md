---
id: stewards-install-door-tests
type: test-deps
status: approved  # maintainer intent act 2026-08-29, in session — reduced from `stewards-plugin-tests` (introduced and ratified by the merge of PR #33) when kodhama-0030 deleted the package those tests covered
depends_on:
  - kodhama-0021-separate-adoption-posture-from-support
  - kodhama-0030-install-door-serves-trellis-only
  - kodhama-0032-the-hub-keeps-only-decisions
  - trellis/decision-0063
owner: agent
---

# Install-door test dependencies

`tests/test_install_door.py` derives from the dependencies above. It covers
the surviving catalog entry's non-support disclosure, the exact catalog
membership `kodhama-0030` D1 fixed, D2's `enabledPlugins` carrier, D3's
absence of the deleted package, the `distribution-scope` three-way mirror,
and the `kodhama-0025` guard against the retired surface/observation shape.

The package, workflow-authoring and issue-skill publication tests retired
with `plugins/kodhama/` under `kodhama-0030`. The specs that contracted them
were deleted outright by `kodhama-0032`, so no spec is named above — an
`id@vN` pin to a file that is not in the tree is worse than no pin. Git
history carries them.
