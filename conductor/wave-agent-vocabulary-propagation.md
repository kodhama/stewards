# Wave: propagate grove's agent vocabulary (adr-0002)

Opened 2026-07-09. Authorization: maintainer, post-merge of
`grove/adr-0002-agent-vocabulary` — "start the whole propagation run."

Scope: `gardener`→`agent`/`grove agent`, `head-gardener`→`dispatcher`
(file rename `head-gardener.md`→`dispatcher.md`, frontmatter `name:`
updated), `furrow`→`run`, everywhere forward-facing. `druid`/`archdruid`
stay sanctioned-conversational per the ADR's own register rule — never
introduced as the defining term in a charter/spec; at most one passing
aside in README/LP copy. Historical/ratified content (adr-0001, adr-0002
itself quoting the old clause, past conductor briefs, ADR-0030 lineage)
is NOT touched — append-only.

**Machinery note** (said out loud, not silently worked around): grove's
own named subagents (`executor`, `conformance-reviewer`, etc.) do not
resolve as native Claude Code subagent types in this session — tested
directly, confirmed unavailable (fixed agent-type list from session
start, doesn't pick up `.claude/agents/*.md` added mid-session). Every
builder lane below is briefed with grove's actual `executor` charter
text embedded verbatim; every review lane is briefed with grove's actual
`conformance-reviewer` charter text embedded verbatim — substance
matches grove's own discipline even though the harness's own bookkeeping
won't label it that way. The conductor (this session) also independently
re-verifies every lane's output before it reaches the maintainer, same
as every wave today.

**Sequencing**: grove's own core rename lands and is reviewed FIRST;
the five consuming repos' installed copies (wisp, kodhama, trellis,
design-system, math-quest) are held until grove's core rename is
actually merged — they'd otherwise be built on branch content that
could still change under review.

## Ledger

- [x] Lane A (grove core) — [grove PR #12](https://github.com/kodhama/grove/pull/12).
      charters/*.md (11, incl. dispatcher rename), .claude/agents/*.md
      (11, same), README.md (+ one druid aside)
- [x] Lane A independent review — conformance-reviewer-charter-briefed,
      separate agent instance. Overall PASS; found one real gap
      (dangling `charter-head-gardener` depends_on + stale paths in
      `specs/0001-contributing-guide.md` + `CONTRIBUTING.md` — neither
      file was in ADR-0002's own enumerated scope list). Verified and
      fixed directly by the conductor, same PR, documented on-PR.
- [ ] Lane B (grove plugin payload sync) — running, sourced from Lane
      A's branch (not yet merged)
- [ ] Lane C (grove LP vocabulary + druid aside) — running, parallel
      with B
- [ ] Lane B/C independent reviews
- [ ] Conductor final spot-check, all grove-side lanes
- [x] Grove core (#12) + plugin (#14) + LP (#13) — all merged by
      maintainer
- Five consumer-install refresh lanes — dispatched in parallel (trellis,
  wisp, kodhama, design-system, math-quest), each a vocabulary
  find-and-replace preserving repo-specific fills:
  - [x] kodhama — merged in `5b61256` ("chore: agent vocabulary sync
        (grove adr-0002)")
  - [ ] trellis — status unverified from here
  - [ ] wisp — status unverified from here
  - [ ] design-system — status unverified from here
  - [ ] math-quest — status unverified from here
- [ ] Consumer lanes' independent reviews
- [ ] Report appended; wave closed pending final merges

## Parked

(none yet)

## Report

(appended at close)
