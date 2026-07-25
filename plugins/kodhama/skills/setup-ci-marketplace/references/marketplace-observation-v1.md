# Marketplace observation version 1

Read this reference only when the caller selected both a `surface_id` and an
observation output path. Runtime emits this record after all registration
checks pass:

```json
{
  "schema_version": 1,
  "host": "codex",
  "surface_id": "github-actions/codex-marketplace",
  "marketplace": {
    "name": "kodhama",
    "repository": "kodhama/stewards",
    "revision": "0123456789abcdef0123456789abcdef01234567"
  },
  "execution": {
    "repository": "kodhama/trellis",
    "commit": "89abcdef0123456789abcdef0123456789abcdef",
    "workflow": ".github/workflows/ci.yml",
    "job": "codex-marketplace",
    "run_id": 123456789,
    "run_attempt": 1,
    "setup_step_id": "kodhama_marketplace_kodhama_codex"
  },
  "observed_at": "2026-07-24T12:34:56.789Z"
}
```

The object and both nested objects are closed; unknown properties are invalid
and every shown property is required.

- `schema_version` is integer `1`.
- `host` is exactly `claude` or `codex`.
- `surface_id` matches `^[a-z0-9][a-z0-9._/-]{0,127}$`.
- `marketplace.name` is nonblank and at most 128 UTF-8 bytes.
- Both repository fields match
  `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`.
- Both revision/commit fields are full 40-character lowercase hexadecimal
  SHAs.
- `execution.workflow` is the selected normalized repository-relative path
  below `.github/workflows/`, ending in `.yml` or `.yaml`, with no `..`.
- `execution.job` is the selected nonblank job key, at most 128 UTF-8 bytes.
- `execution.run_id` and `execution.run_attempt` are positive integers.
- `execution.setup_step_id` matches
  `^[A-Za-z_][A-Za-z0-9_-]{0,127}$`.
- `observed_at` is a real UTC instant with exactly millisecond precision:
  `YYYY-MM-DDTHH:mm:ss.sssZ`.

Populate runtime values from `GITHUB_REPOSITORY`, `GITHUB_SHA`,
`GITHUB_RUN_ID`, and `GITHUB_RUN_ATTEMPT`. The selected workflow path, job key,
step id, host, marketplace inputs, and surface id are authoring constants.
Generate `observed_at` at runtime in UTC. Validate required variables and
values before writing.

Create the parent directory, write JSON to a temporary sibling, validate it
with an inline standard-library script, then atomically rename it to the
selected output path. Install no validator dependency. A trap removes the
temporary file. If any provenance check, variable, serialization, structural
validation, or rename fails, the selected output path must not exist.

This observation records marketplace registration only. It has no plugin,
result, support, availability, approval, release, qualification, or
effective-state field.
