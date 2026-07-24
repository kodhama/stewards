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
- [ ] Pass the exact-candidate Codex behavioral canary against the marketplace
  candidate. Run `30093655291` installed and digest-verified the candidate but
  could not invoke Codex because Wisp has no `CODEX_API_KEY` Actions secret.
- [ ] Tag the tested commit `wisp-v0.2.1-rc.1`.
- [x] Publish a separately named GitHub test prerelease that says
  `unqualified dogfood candidate` without claiming the gated family tag.

### Stewards install door

- [x] Add one thin Wisp `git-subdir` pointer to the Claude catalog.
- [x] Add the equivalent thin pointer to the Codex catalog.
- [x] Keep product code, versions, and behavioral claims in Wisp.
- [x] Validate both catalog JSON files.
- [x] Install the exact candidate through a clean Codex marketplace home.
- [ ] Add the product surface contract and Stewards availability records
  required by decisions 0015 and 0016.
- [ ] Merge the Stewards catalog change only after the product contract,
  canonical release tag, and availability records exist.

## Report

Wisp PR [#30](https://github.com/kodhama/wisp/pull/30) merged as
`9acddd68a0a03894589c0165215f1a4d882d5564` after Node 20/22/24 and the
deterministic container E2E passed. The product metadata identifies
`0.2.1-rc.1` and deliberately resets qualification to `pending`.

Wisp PR [#32](https://github.com/kodhama/wisp/pull/32) repaired the canary
workflow's runner-path scoping. Candidate canary
[30093655291](https://github.com/kodhama/wisp/actions/runs/30093655291)
then installed version `0.2.1-rc.1` from this branch and matched bundle
SHA-256
`28fdf9d945a241f7fb448732d25ac696c92ee32f08fa631d1ed4235a76a8680e`.
Its behavioral phase failed closed because the Wisp repository has no
`CODEX_API_KEY` Actions secret.

The independently named
[`wisp-test-v0.2.1-rc.1`](https://github.com/kodhama/wisp/releases/tag/wisp-test-v0.2.1-rc.1)
GitHub prerelease records the dogfood candidate without creating the
qualification-gated `wisp-v0.2.1-rc.1` family tag. A separate isolated Codex
home registered this marketplace branch, installed `wisp@kodhama` as
`0.2.1-rc.1`, and reproduced the expected bundle digest.

Pending: a passing behavioral canary, Wisp's product surface contract and
canonical release gate, the immutable family tag, Stewards availability
records, and canonical catalog merge.
