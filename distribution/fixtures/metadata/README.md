---
id: stewards-family-distribution-fixtures
type: fixture-index
status: gated
depends_on: [kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v1]
owner: agent
updated: 2026-07-24
---

# Family distribution fixtures

`manifest.json` is the machine-readable index of fixtures that are currently
materialized and executed. Each row names its exact test function, expected
exit class, and guarded scenario or requirement. The executable vectors live
in `distribution/tests/test_distribution.py`; its spec-anchored tests
construct clean temporary repositories where mutable package or derivative
state is required. Deferred release-engine fixtures are recorded only in
`distribution/IMPLEMENTATION-STATUS.md`, not counted here.
