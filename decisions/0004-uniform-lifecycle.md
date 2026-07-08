---
id: kodhama-0004-uniform-lifecycle
type: decision
status: approved  # ratified by PR #8 merge (2026-07-08)
depends_on: [kodhama-0003-family-naming]
owner: agent
updated: 2026-07-08
provenance: maintainer redirect during the grove-install wave — "I know about the variability and how it's consistent with trellis design, but I wanted these states the same for all repos." Supersedes the trellis carve-out recorded in the 2026-07-07 status-vocabulary consolidation.
---

# Decision: one artifact lifecycle for every family repo — including trellis-self

**Decision.** Every kodhama-family repo — kodhama, trellis (including
its own self-application), grove, wisp, design-system — uses the same
artifact lifecycle and the same mechanics:

- **Enum:** `draft → gated → approved (→ superseded)`.
- **`gated`** = self-checked, agent-consumable. Consuming a `draft` is
  forbidden (no `gated`/`approved` artifact may `depends_on` a `draft`).
- **`approved`** = human PR merge. Nobody writes `approved` inside the
  PR's own diff; a post-merge bump commit records the act. (This
  supersedes trellis-self's in-diff flip mechanic from its
  decision-0022 — one mechanic family-wide, not two.)
- **`superseded`** = forward pointer required; ratified content never
  edited in place.

**What this supersedes.** The 2026-07-07 status-vocabulary
consolidation declared one vocabulary for the family but deliberately
left trellis-self on its native `draft → ratified` (trellis
decision-0037 had considered and declined a `gated` ratchet for
itself). The maintainer has now decided uniformity outweighs that
variability: same states, same words, everywhere. The kodhama
`.trellis/profile.md` sentence recording the carve-out gains a forward
pointer to this decision (same PR).

**What this does NOT do.** No historical artifact is rewritten
(append-only): trellis's 40+ `ratified` artifacts keep their frontmatter;
`ratified` reads as `approved` under the equivalence decision-0037
already declares. Only forward artifacts use the family enum. The bulk
relabel was considered and rejected — it would forge history for zero
information gain.

## Execution (trellis-side, its own PR in its own repo)

1. A trellis decision superseding **in part** decision-0037 (the
   trellis-self enum choice) and decision-0022 (the in-diff flip),
   adopting the family enum + post-merge-bump mechanic for trellis's
   own `decisions/` and `specs/` going forward.
2. `ratify-guard` CI updated: a non-draft PR may not introduce or touch
   an artifact left at `status: draft` (unchanged), accepts `gated` as
   the mergeable state, and never sees `approved` written in-diff.
3. `.trellis/profile.md` gains the same "Lifecycle mapping" section the
   other four repos carry (the grove-install lane found trellis is the
   one family repo without it).
4. CLAUDE.md's Artifacts bullet ("draft → ratified → approved") fixed to
   the family enum — the doc drift the install lane flagged.
5. `core/rubrics/artifact-contract.md` check 2 and the native
   corpus-reviewer instance read the enum from the repo's declared
   lifecycle mapping (which, post-0004, is the same everywhere).

## Acceptance criteria

- **AC1** All five family repos' `.trellis/profile.md` carry the same
  lifecycle-mapping section, trellis included.
- **AC2** The trellis-side decision is merged; `ratify-guard` passes on
  a `gated` artifact and the repo's forward artifacts use the family
  enum.
- **AC3** kodhama's profile carve-out sentence carries its forward
  pointer to this decision.
- **AC4** No pre-existing artifact's status frontmatter is rewritten.
- **AC5** The paused trellis grove-install resumes with grove's
  canonical status language unchanged (no per-repo rewrite needed).

## Open questions (parked, ≤3)

- Do the post-merge bump commits in trellis need their own CI check
  (approved-only-after-merge), or is review discipline enough? (Decide
  when the trellis-side PR lands.)

## Self-check (gate)

Maintainer intent quoted in provenance; the superseded carve-out
located and quoted from the recorded consolidation; both prior trellis
decisions (0022, 0037) named with exactly which part each loses;
append-only preserved with the rejected alternative recorded; ACs give
pass/fail; execution enumerated and scoped to a trellis-side PR the
human ratifies separately. Promote `draft → gated`. `approved` = human
merge of this PR.
