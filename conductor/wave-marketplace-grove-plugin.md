# Wave: org marketplace + grove plugin (executes kodhama-0002 §2–§3)

Opened 2026-07-08. Authorization: maintainer — "go for the marketplace
and grove plugin pass." Scope: decision 0002's remaining delivery items —
the org marketplace in `kodhama/kodhama` (§2, incl. the CLAUDE.md
front-door line) and grove shipping as plugin `grove@kodhama` with a
composing `/grove:setup` skill (§3, incl. demoting hand-vendoring to
manual path — AC2). Wisp's npm/npx channel (§4) stays parked until wisp
releases, per the matrix.

Mechanics verified against official docs before building: cross-repo
subdirectory plugins use the `git-subdir` source (`url` + `path`);
marketplace `name: "kodhama"` gives `X@kodhama` installs — 0002's parked
name-string question, answered. Trellis's shipped plugin
(`plugins/trellis`, setup/remove skills, vendored `reference/` payload)
is the family pattern grove mirrors.

Model economy: grove plugin lane on Sonnet 5 against a conductor-authored
spec; meta-repo slice by the conductor directly. PR-first everywhere.

## Ledger

- [x] kodhama: `.claude-plugin/marketplace.json` (name `kodhama`;
      trellis + grove via git-subdir) + CLAUDE.md front-door line —
      [kodhama PR #6](https://github.com/kodhama/kodhama/pull/6), MERGED
      by maintainer same day
- [x] grove: `plugins/grove/` (plugin.json, `/grove:setup` composing
      skill, reference payload) + README §Adopting demoted to manual
      path — [grove PR #5](https://github.com/kodhama/grove/pull/5)
- [x] Conductor: independent verification — see report
- [x] Report appended; wave closed pending grove #5 merge

## Parked

- **"Grove should operate under trellis?"** (maintainer, this wave's
  authorization message, self-deferred: "we can decide that later").
  Current posture kept: trellis recommended-not-required (grove README
  step 4; the setup skill points at `trellis@kodhama` without
  installing it). Needs a decision only if that posture should harden.
- **Follow-up queued, not this wave:** install grove on all projects
  (maintainer asked to do it or ask for help after this pass — the
  placeholder interviews likely need the maintainer per project).

## Report

Closed 2026-07-08. The marketplace half merged (kodhama #6) before this
brief was even committed — a ledger-lag deviation, owned: the brief
existed locally from wave open but rode to the repo only with this
commit, because the meta repo's PR-first rule makes mid-wave ledger
commits a PR each. Accepting brief-lands-at-close as the practice going
forward.

**Marketplace** — merged. `/plugin marketplace add kodhama/kodhama` is
live; `name: "kodhama"` answers 0002's parked name-string question;
grove's entry resolves once grove #5 merges (order noted in the PR).

**Grove plugin** — [grove PR #5](https://github.com/kodhama/grove/pull/5),
open, conductor-verified: diff scope 17 files / +965 additive (plugins/
tree + README §Adopting only); reference payload drift-free against the
canonical `.claude/agents/` (checked file-by-file, modulo the one
vendoring header line); setup skill reviewed line-by-line and endorsed
(compose-not-generate, interview-per-token, honest-gap as first-class
resolution with wisp's B4 install cited as precedent, idempotent managed
block, telemetry optional, trellis recommended-never-installed — the
parked posture kept). AC2 satisfied at merge (vendoring demoted to
"Manual path", preserved verbatim).

**Incident, owned by the conductor:** a repo-sync loop ran
`git checkout main` inside the plugin lane's live workspace mid-run. The
lane self-recovered via reflog (its commit briefly sat on local `main`;
`origin/main` was never touched — independently confirmed, `4cdfec5`
before and after), documented the incident in its PR, and finished
clean. Root-cause rule adopted: **a conductor never runs git mutations
in a repo an active lane owns** — sync loops must exclude lane
workspaces (this wave's install lanes already read grove via an
immutable `git archive` snapshot instead).

**Parked → maintainer:** AC1's live install smoke (this CLI build has no
scripted marketplace-add; one interactive `/plugin marketplace add
kodhama/kodhama` + `/plugin install grove@kodhama` after grove #5
merges). The grove-under-trellis posture question remains parked as
recorded above.
