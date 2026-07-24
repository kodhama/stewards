---
id: stewards-provisioner-fixtures-0001
type: fixture-catalog
status: gated
depends_on: [kodhama-spec-0002-bounded-pre-agent-provisioner@v1]
owner: agent
updated: 2026-07-24
---

# Provisioner fixtures

These offline requests exercise the current fail-closed boundary. The
authoritative `distribution/provisioners.json` contains no candidate or
verified route, so no fixture claims installation, adapter behavior, or
promotion evidence.

`claude-route-not-found.json` and `codex-route-not-found.json` prove that both
registered hosts reach typed identity-resolution failure without host-state
mutation. `version-range.json` and `unused-reference.json` prove validation
precedence over the absent route.

Positive install, idempotency, preservation, launch-interception, and retained
two-run fixtures remain unavailable until an exact candidate or verified route
is added through the spec-0001 availability authority.
