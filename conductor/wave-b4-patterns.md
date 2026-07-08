# Wave: B4 (grove as wisp's operating model) + DS patterns.md staleness fix

Opened 2026-07-08. Authorization: maintainer — "Do B4 and the parked
finding about patterns.md now." B4 is the suite-lift plan's last Lane B
step ("viz work items run as [grove] furrows; [grove] is installed in
the viz repo as operating model"). The patterns.md item is the parked
finding from the T3+B3 wave (DS `v0.1.0` shows the pre-decision-0041
install example), un-parked by the maintainer's instruction — fixed on
DS main; reaches consumers at the next tag cut (T2's), deliberately NOT
cutting a tag here.

Model economy: B4 on Sonnet 5 (execution lane); the patterns.md fix is a
two-line mechanical change done by the conductor directly (dispatching a
lane for it would be ceremony). Conductor verifies B4 independently.
PR-first policy applies to both repos.

## Ledger

- [x] B4: grove's agent definitions + grove-status skill vendored into
      wisp with placeholders filled with wisp-real values; artifact
      stores (decisions/, specs/) seeded; CLAUDE.md declares the
      operating model — [wisp PR #6](https://github.com/kodhama/wisp/pull/6)
- [x] DS: patterns.md install example → `kodhama/tap/trellis` (both
      occurrences) — [design-system PR #3](https://github.com/kodhama/design-system/pull/3)
- [x] Conductor: independent verification of B4 — see report
- [x] Report appended; wave closed pending PR merges

## Parked

(none)

## Report

Executed 2026-07-08. B4 on Sonnet 5 (≈132k subagent tokens / 93 tool
uses); patterns.md fix by the conductor directly (two-line mechanical
change, PR as the review seam).

**B4 — landed as [wisp PR #6](https://github.com/kodhama/wisp/pull/6)
(open, not merged).** Ten gardener roles + README vendored into
`.claude/agents/`, `grove-status` skill vendored with the vendor path
resolved to `.` (wisp reports through its own `emit.ts` — the recursion
is documented in the skill and CLAUDE.md), minimal `decisions/` +
`specs/` stores seeded, CLAUDE.md operating-model section added above
the untouched trellis block. Conductor verification, not builder
claims: diff scope 15 files / +806 additive-only; protected files
(protocol/bus/emit/server/github/dashboard/docs/package*) zero-diff;
zero `<[A-Z_]+>` markers left in `.claude/`; zero old family names;
fresh `npm test` 36/36; `tsc --noEmit` clean. Honest-gap placeholder
handling endorsed: where wisp has no rubric/parked-store/PR-contract,
the vendored files SAY so instead of inventing process — grove's own
repo has the same gaps. Three documented deviations from a literal
vendor (live GitHub charter URLs instead of dangling relative paths;
illustrative angle-bracket examples also resolved; resolved
`## Placeholders` sections removed per the math-quest precedent) — all
reasonable, all stated in the PR.

**patterns.md — landed as
[design-system PR #3](https://github.com/kodhama/design-system/pull/3)
(open, not merged).** Both occurrences now `kodhama/tap/trellis`.
Stated caveat: consumers read at pinned tags, so `v0.1.0` stays stale
by design — the fix ships with the next tag cut, which T2 owns (along
with the `identity/` coverage gap).

**Lane B is now fully dispatched (B1–B4).** With these merged, the
suite-lift plan's remaining open items: T2 (in-flight design process,
owing the new tag + lore layer + this patterns fix's tag), Lane D
(untriggered, non-blocking research), and the math-quest-side human
gates (feature-branch merge; ADR-0030 bump).
