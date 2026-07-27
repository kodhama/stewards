---
name: setup-ci-marketplace
description: Add an immutable, verified Claude Code and/or Codex marketplace checkout and registration block to selected repository-owned GitHub Actions jobs. Use when asked to provision a plugin marketplace in CI, prepare direct Claude or Codex CLI jobs to discover plugins, or audit whether such setup is already present.
---

# Set up a plugin marketplace in GitHub Actions

Author marketplace registration in repository-owned workflows. This skill
changes CI configuration only. It never installs a CLI or plugin, launches a
host, runs a product test, claims support, or treats authored YAML as evidence.

Version 2 supports direct invocations provisioned as exactly Claude Code `2.1.199`
or Codex CLI `0.145.0`. An opaque host action is detected and
reported as unsupported; do not split, wrap, or guess its inputs.

## Non-negotiable boundaries

- Work only below the trusted repository's `.github/workflows/` directory.
- Preserve triggers, permissions, concurrency, environments, secrets,
  matrices, conditions, timeouts, unrelated steps, comments, and formatting.
- Never edit an external reusable workflow. A repository-local reusable
  workflow is editable only when every local caller is selected and all
  callers supply identical marketplace and host-state inputs.
- Do not copy or create authentication, trust, session state, or credentials.
- Do not infer the target host from the host invoking this skill.
- Do not choose a plugin, install a plugin, choose a test, or install a CLI.
- Any ambiguity, unsupported version, unowned equivalent setup, or owned-id
  collision means **no edit** to that target and a precise report.

## 1. Inspect and classify

Read all `.yml` and `.yaml` files below `.github/workflows/`. For caller-selected
jobs—or detected candidates the caller will confirm—record:

- direct `claude` and `codex` invocations;
- their caller-owned CLI provisioning steps and exact pinned versions;
- plugin-install or host-invocation steps that setup must precede;
- job and relevant step `env` mappings;
- local and external reusable-workflow relationships;
- opaque host actions, dynamic wrappers, and existing marketplace-like steps;
- canonical Kodhama-owned ids already present.

A direct shell invocation is supported only when the same job has a
caller-owned prerequisite proving the exact supported version. An official or
third-party action that invokes the host internally is an **opaque host
action**, not a direct target. An external reusable workflow is always
read-only.

If the relevant CLI prerequisite, first product-owned plugin-install step, or
first host invocation has a step-level `if:`, classify the target as
ambiguous and make no edit. Version 2 does not copy or combine step conditions.
A job-level `if:` remains supported because it governs all steps together.

## 2. Resolve and confirm the plan

Before editing, echo one complete plan and obtain explicit confirmation. The
plan must identify:

1. repository root and exact workflow/job keys;
2. `claude`, `codex`, or both for every job;
3. marketplace name matching `^[a-z0-9][a-z0-9-]{0,63}$`;
4. GitHub `owner/repository`;
5. a full 40-character lowercase marketplace commit SHA;
6. the caller-approved full 40-character `actions/checkout` commit;
7. the existing exact CLI prerequisite for each host;
8. the exact host-state environment mapping inherited by registration and the
   later invocation (empty means the job default).

Reject branches, tags, floating refs, unknown CLI versions, non-GitHub
marketplaces, incompatible shared-callee inputs, and partial
inputs. Never silently select a value. If discovery was requested, present the
candidates and classifications for confirmation.

## 3. Check ownership and convergence

For marketplace `<m>` and host `<h>`, Kodhama owns only:

- `kodhama_marketplace_<m>_checkout`;
- `kodhama_marketplace_<m>_<h>`;
- `Kodhama marketplace: checkout <m>`;
- `Kodhama marketplace: register <m> for Claude`; and
- `Kodhama marketplace: register <m> for Codex`.

The path is `.kodhama/marketplaces/<m>`. Preserve hyphens in `<m>` and reject
any name that cannot form those identifiers.

Parse the YAML semantically. If all owned steps already equal the confirmed
plan—including ids, names, action pin, checkout inputs, order, commands,
workspace-root working directory and environment—the target
is idempotent and converged:
write no file, preserving every byte. If an owned id differs, or an unowned
block appears equivalent, report a collision and make no target edit. Never
adopt, rewrite, or delete caller-owned setup implicitly.

## 4. Author the smallest insertion

Use the existing workflow's YAML style and edit only the smallest contiguous
step sequence. One checkout is shared by both hosts when marketplace and
revision match. Put each host registration after its CLI prerequisite and the
marketplace checkout, and before that host's first plugin-install or invocation
step. Keep Claude and Codex registration and host state separate.

The checkout step is:

```yaml
- name: "Kodhama marketplace: checkout <m>"
  id: kodhama_marketplace_<m>_checkout
  uses: actions/checkout@<caller-approved-40-character-commit>
  with:
    repository: <owner/repository>
    ref: <marketplace-40-character-commit>
    path: .kodhama/marketplaces/<m>
    persist-credentials: false
```

Each registration step sets
`working-directory: ${{ github.workspace }}` and must fail closed before
invoking its host:

1. obtain the checkout origin with
   `git -C .kodhama/marketplaces/<m> remote get-url origin`;
2. normalize only one terminal `.git`;
3. compare it exactly with `https://github.com/<owner>/<repository>`;
4. obtain `git -C .kodhama/marketplaces/<m> rev-parse HEAD`;
5. compare it exactly with the selected revision; and
6. leave nothing behind if any check fails.

These are the checkout-scoped forms of `git remote get-url origin` and
`git rev-parse HEAD`; do not inspect the product checkout by mistake.

For Claude, use exactly:

```text
claude plugin marketplace add ./.kodhama/marketplaces/<m> --scope local
claude plugin marketplace list --json
```

Parse the JSON list and find marketplace `<m>`. Use its string `path`, falling
back to string `installLocation` only when `path` is absent. Resolve that value
and the checkout with the filesystem real-path operation and require
byte-identical absolute results. Missing, non-string, nonexistent, or
non-matching roots fail; accept no other field.

For Codex, use exactly:

```text
codex plugin marketplace add ./.kodhama/marketplaces/<m> --json
codex plugin marketplace list --json
```

Parse the JSON object's `marketplaces` array and find marketplace `<m>`. Its
`root` must be a string whose filesystem real path byte-equals the checkout's
real path. Missing, non-string, nonexistent, or non-matching roots fail;
accept no other field. Command success alone is insufficient for either host.

Use a temporary file for listing output and remove it on exit. Quote shell
values. Do not print environment values or secrets. The registration step
inherits the confirmed host-state `env` mapping exactly.


## 5. Verify and report

Re-read every changed YAML file. Confirm that the semantic target block matches
the plan, remains after each CLI prerequisite, and precedes the first
corresponding host/plugin invocation. Inspect the diff for unrelated changes
and secret exposure. Reapply the semantic comparison to prove idempotence; do
not rewrite a converged file.

Report:

- every inspected workflow;
- every changed workflow/job and every already-converged target;
- host classification per selected job;
- marketplace name, repository, and immutable revision per host;
- pinned CLI prerequisite and confirmed host-state mapping;
- generated checkout and host step ids;
- every ambiguous, external, conflicting, unsupported, collision, or skipped
  target with its reason; and
- whether files changed.

State explicitly that workflow authoring did not install a plugin, run a host
or product test, or establish surface support.
