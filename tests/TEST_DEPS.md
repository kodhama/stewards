---
id: stewards-install-door-tests
type: test-deps
status: approved  # maintainer intent act 2026-08-29, in session — reduced from `stewards-plugin-tests` (introduced and ratified by the merge of PR #33) when kodhama-0030 deleted the package those tests covered
depends_on:
  - kodhama-0021-separate-adoption-posture-from-support
  - kodhama-0030-install-door-serves-trellis-only
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
with `plugins/kodhama/` under `kodhama-0030`, and with them
`kodhama-spec-0004@v5`, `kodhama-spec-0005@v13`, `kodhama-0018` and
`kodhama-0020` as live dependencies — all four now describe an artifact that
does not exist. The observation validator and its tests retired earlier with
`kodhama-0025`.
