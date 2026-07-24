# Wave: publish the Wisp 0.2.1 release candidate for dogfooding

Opened 2026-07-24. Authorization: the maintainer requested a release for
testing and explicitly deferred a more structured release process.

This is staged distribution, not a product-support claim. Wisp
`0.2.1-rc.1` keeps its product qualification result `pending`; Claude
qualification remains tracked by Wisp issue #25.

## Lanes and gates

### Wisp product

- [x] Merge Wisp PR #30 with version `0.2.1-rc.1`.
- [x] Require Node 20/22/24 and deterministic container E2E checks to pass.
- [ ] Run the exact-candidate Codex canary against the marketplace candidate.
- [ ] Tag the tested commit `wisp-v0.2.1-rc.1`.
- [ ] Publish a GitHub prerelease that says `unqualified dogfood candidate`.

### Stewards install door

- [x] Add one thin Wisp `git-subdir` pointer to the Claude catalog.
- [x] Add the equivalent thin pointer to the Codex catalog.
- [x] Keep product code, versions, and behavioral claims in Wisp.
- [x] Validate both catalog JSON files.
- [ ] Install the exact candidate through a clean Codex marketplace home.
- [ ] Merge the Stewards catalog change only after Wisp lands.

## Report

Wisp PR [#30](https://github.com/kodhama/wisp/pull/30) merged as
`9acddd68a0a03894589c0165215f1a4d882d5564` after Node 20/22/24 and the
deterministic container E2E passed. The product metadata identifies
`0.2.1-rc.1` and deliberately resets qualification to `pending`.

Pending: exact-candidate canary, immutable tag, GitHub prerelease, clean
marketplace install, and Stewards merge.
