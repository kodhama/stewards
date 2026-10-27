# stewards

The **stewards** are [kodhama](https://github.com/kodhama/kodhama)'s worker collective — the scaffolding that tends the forest's trees (the products) and tends itself. This repo is their coordination hub. It continues the operational role that used to live in `kodhama/kodhama`, relocated here (per `kodhama-0009`) so the kodhama repo can be the forest-spirit front door.

Its two long-standing jobs are cross-collective **decisions** (`decisions/`) and the **install door** (the collective's canonical install repository per `kodhama-0002`, `kodhama-0012`, and `kodhama-0017`). The conductor seat and the spec corpus were deleted by `kodhama-0032`; git history is their archive. That is what the repo is for, not a closed list of what it contains: **product truths live in product repos, and only genuinely cross-collective content lands here.**

<!-- distribution-scope:begin -->
The repository root is the `kodhama` command (`package.json`, `bin/`,
`src/`), run as `npx -y github:kodhama/stewards#v<version>`. It installs,
updates, checks and removes a tool's skills for Claude and Codex by cloning
that tool's own repository at one of the tool's tags. It bundles no tool's
content, and its own tag never pins a tool's tag. The install door also
includes the host-native Claude and Codex catalogs. Both catalogs list
`trellis` and nothing else, sourced from the repository that owns it. This
repository **originates no plugin**: the `kodhama` package it used to carry
was deleted along with its listing (`kodhama-0030`), and grove and wisp were
delisted in the same act. That is a description of present contents, not a
scope: it moves when the contents move. Neither the command nor the catalogs
certify product releases or support. Apart from the command's own tag
lookup and `kodhama.json` contract (`kodhama-0033`), the repository owns no
universal version, tag, release-history, approval, runtime-sandbox,
cross-repository-resolution, or effective-support machinery.
<!-- distribution-scope:end -->

Run the command as `npx -y github:kodhama/stewards#v<version> <verb>`. `install <tool>[#<tag>]` copies a tool's skills into Claude's and Codex's skills folders, `update <tool>[#<tag>]` moves them to another tag (the newest by default), `check [<tool>]` compares them with the lock without touching the network, and `remove <tool>` moves them out to `prev/`. `--scope user|project` picks your own folders (the default) or the current git repo's, `--harness claude|codex` limits `install` and `remove` to one harness, and `install --migrate` first takes a clashing plugin enable out of your user settings, keeping a receipt.

The stewards: [trellis](https://github.com/kodhama/trellis) (governance) · [grove](https://github.com/kodhama/grove) (agent swarm) · [wisp](https://github.com/kodhama/wisp) (runtime observability) · [design-system](https://github.com/kodhama/design-system) (brand) · [homebrew-tap](https://github.com/kodhama/homebrew-tap) (delivery).

**Spore remains retired.** [Decision `kodhama-0019`](decisions/0019-spore-handoff-capsules.md)
records only a future direction for the name: portable, target-specific
handoff capsules for vendoring selected Kodhama functionality elsewhere. It
does not readmit a product or authorize implementation, delivery, or support.

They tend the trees (products) — [math-quest](https://github.com/kodhama/math-quest) today — and tend themselves. The whole is the forest, kodhama; see [kodhama/kodhama](https://github.com/kodhama/kodhama) for the full picture (topology in `kodhama-0009`).
