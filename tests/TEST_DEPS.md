---
id: stewards-plugin-tests
type: test-deps
status: approved  # introduced and ratified by the maintainer's merge of PR #33
depends_on:
  - kodhama-spec-0004-ci-marketplace-setup-skill@v5
  - kodhama-0018-stewards-dual-host-plugin-package
  - kodhama-0021-separate-adoption-posture-from-support
  - trellis/decision-0063
owner: agent
---

# Kodhama plugin test dependencies

The package, workflow authoring, and preview catalog tests derive from the
dependencies above. The observation validator and its tests retired with
`kodhama-0025`.
