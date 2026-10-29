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
