---
id: stewards-family-distribution-fixtures
type: fixture-index
status: gated
depends_on: [kodhama-spec-0001-family-plugin-release-and-distribution-metadata@v1]
owner: agent
updated: 2026-07-24
---

# Family distribution fixtures

`manifest.json` is the machine-readable fixture authority. Each row names the
spec fixture, command, expected exit class, and guarded scenario or
requirement. The executable vectors live in
`distribution/tests/test_distribution.py`; its spec-anchored tests construct
clean temporary package repositories so tag, mutation, and no-write cases do
not depend on mutable checked-in Git state.
