---
id: kodhama-0011-spore-plugin-channel
type: decision
status: gated  # → approved on ratifying PR merge (status bumped with the PR number before merge)
depends_on: [kodhama-0001-family-delivery, kodhama-0002-delivery-channels, kodhama-0010-add-spore]
owner: agent
updated: 2026-07-22
provenance: maintainer request 2026-07-22 to package spore as a marketplace plugin, immediately after its admission to the stewards (kodhama-0010). Stated goal — make the skills available to every user on a machine, with the install left to each user.
---

# Decision: spore gains a Claude Code plugin delivery channel

**Decision.** spore is packaged as the **`spore@kodhama`** Claude Code plugin
and listed in the `@kodhama` marketplace manifest
(`stewards/.claude-plugin/marketplace.json`). This is the follow-up
`kodhama-0010` named — *"if it is ever packaged as a plugin, a marketplace entry
is the follow-up, not this decision."* 0010 admitted spore to the stewards
without a plugin; this decision adds the channel.

## What ships

- **Repo layout** (`git-subdir`, matching grove/trellis): the plugin root is
  `kodhama/spore` → `plugins/spore/`, manifest at
  `plugins/spore/.claude-plugin/plugin.json`. The five skills moved under
  `plugins/spore/skills/`; the shared `_lib` helper stays beside them (the skill
  loader skips `SKILL.md`-less directories), so one source of truth serves both
  the plugin and the repo's `install.sh`.
- **Marketplace entry**: appended after grove in the manifest `plugins` array —
  `{ source: git-subdir, url: kodhama/spore, path: plugins/spore }` — and the
  manifest description gains `spore (session drivers)`.
- **Skill namespace**: skills load as `spore:<skill>` when the plugin is enabled
  (`spore:fork-here`, …); `install.sh` still offers a bare-name
  `~/.claude/skills/` install for local development.

## Availability model (the "all users on a machine" question)

Claude Code plugins are **per-user** (`~/.claude/`); there is no native
all-users install. The marketplace makes spore **available** to every user on a
machine, and each user opts in with `/plugin install spore@kodhama` — *available
to all, installed by each*. An admin who wants it enabled for everyone uses
managed settings (`extraKnownMarketplaces` + `enabledPlugins`) or per-user
provisioning; spore ships the plugin, not a machine-wide installer. That step is
left to the operator — documented in the repo README, not automated.

## Delivery channel, recorded (`kodhama-0002`)

spore's channels are now: **own public repo** (source, MIT) + **`@kodhama`
marketplace plugin** (`git-subdir`). It is not on the Homebrew tap and ships no
binary — it is macOS shell + markdown skills, so the plugin/marketplace channel
is the whole delivery surface, consistent with the family's per-artifact channel
matrix (`kodhama-0001`/`0002`).

## Self-check (gate)

Verified this session against sources: the live `@kodhama` marketplace resolves
from `kodhama/stewards` (this machine's `known_marketplaces.json` →
`repo: kodhama/stewards`; `kodhama/kodhama` carries no manifest), so the entry
lands in stewards. The `git-subdir` / `plugin.json` / skill-namespacing /
per-user-scope facts were confirmed against the Claude Code plugin docs
(plugins-reference, plugin-marketplaces, settings). The `plugins/spore/` layout,
`plugin.json` validity, `_lib` resolution, and `install.sh` from the new path
were all exercised before this landed. `draft → gated`; `approved` = human merge
of the ratifying PR.
