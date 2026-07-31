#!/usr/bin/env bash
# Provision the kodhama issue taxonomy: org-level issue types + per-repo labels.
#
# Dry-run by default. Nothing is created or changed without --apply.
# This script NEVER deletes a label. Redundant stock labels are reported only.
#
#   ./seed-issue-taxonomy.sh                        # plan for every family repo
#   ./seed-issue-taxonomy.sh --repo grove           # plan for one repo
#   ./seed-issue-taxonomy.sh --repo grove --apply   # execute for one repo
#   ./seed-issue-taxonomy.sh --types-only --apply   # org issue types only
#   ./seed-issue-taxonomy.sh --labels-only           # labels, skip types
#   ./seed-issue-taxonomy.sh --repo X --force        # seed a repo with no backlog
#
# Requires: gh, with scopes `repo` (labels) and `admin:org` (issue types).
set -euo pipefail

ORG="kodhama"
APPLY=0
TYPES_ONLY=0
LABELS_ONLY=0
FORCE=0
REPOS=()

ALL_REPOS=(trellis grove wisp math-quest design-system kodhama stewards sdd-gauntlet homebrew-tap)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --org)         ORG="$2"; shift 2 ;;
    --repo)        REPOS+=("$2"); shift 2 ;;
    --apply)       APPLY=1; shift ;;
    --types-only)  TYPES_ONLY=1; shift ;;
    --labels-only) LABELS_ONLY=1; shift ;;
    --force)       FORCE=1; shift ;;
    -h|--help)     sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
[[ ${#REPOS[@]} -eq 0 ]] && REPOS=("${ALL_REPOS[@]}")

if [[ $APPLY -eq 0 ]]; then
  echo "DRY RUN — nothing will be changed. Re-run with --apply to execute."
  echo
fi

run() {  # run <description> <command...>
  local desc="$1"; shift
  if [[ $APPLY -eq 1 ]]; then
    if "$@" >/dev/null 2>&1; then echo "  ✓ $desc"
    else echo "  ✗ $desc  (failed — see notes below)"; fi
  else
    echo "  + would create: $desc"
  fi
}

# ---------------------------------------------------------------- issue types

# name|color|description   — Task, Bug, Feature ship with every org already.
CUSTOM_TYPES=(
  "Research|purple|An open question to answer. The deliverable is a finding, not a change"
  "Decision|orange|A choice that must be made and recorded"
  "Epic|green|Children that ship separately, plus the guarantee the set is coherent and complete"
)

seed_types() {
  echo "== org issue types: $ORG =="

  if ! gh auth status 2>&1 | grep -q 'admin:org'; then
    echo "  ! your gh token lacks the 'admin:org' scope — creating types will fail."
    echo "    fix with:  gh auth refresh -h github.com -s admin:org"
    echo
  fi

  # name<TAB>is_enabled<TAB>id — a DISABLED type still appears here and still
  # cannot be set, so name-only matching would report it provisioned forever.
  local all
  all="$(gh api "/orgs/$ORG/issue-types" --jq '.[] | [.name, (.is_enabled|tostring), (.id|tostring)] | @tsv' 2>/dev/null || echo "")"

  for spec in "${CUSTOM_TYPES[@]}"; do
    IFS='|' read -r name color desc <<< "$spec"
    local row enabled id
    row="$(awk -F'\t' -v n="$name" '$1==n{print; exit}' <<< "$all")"
    if [[ -z "$row" ]]; then
      run "type $name" gh api --method POST "/orgs/$ORG/issue-types" \
        -f "name=$name" -f "color=$color" -f "description=$desc" -F is_enabled=true
      continue
    fi
    enabled="$(cut -f2 <<< "$row")"; id="$(cut -f3 <<< "$row")"
    if [[ "$enabled" == "true" ]]; then
      echo "  = $name (exists, enabled)"
    else
      echo "  ! $name exists but is DISABLED — present in the API, unusable on an issue"
      run "enable $name" gh api --method PATCH "/orgs/$ORG/issue-types/$id" -F is_enabled=true
    fi
  done
  echo
}

# --------------------------------------------------------------------- labels

# name|color|description
LABELS=(
  "stage: triage|fef2c0|Not yet dispatchable — noticed, or accepted and still being worked out"
  "stage: ready|0e8a16|Dispatchable; what had to be decided is decided"
  "stage: active|1d76db|Started, not yet done"
  "stage: review|5319e7|Done, not yet verified"

  "facing: user|0e8a16|Changes what a consumer of this repo gets"
  "facing: system|5319e7|Changes only how this repo is built or maintained"

  "severity: blocker|b60205|Someone is stopped, with no way through"
  "severity: broken-feature|d93f0b|A path is unusable or misleading; the default path still works"
  "severity: papercut|fef2c0|Annoying, cosmetic, or has a workaround"

  "priority: urgent|b60205|Drop other work"
  "priority: high|d93f0b|Next up, ahead of unlabelled work"
  "priority: low|c5def5|Wanted, ranked below normal"

  "blocked|b60205|Blocked by something that is not an issue (issue-to-issue is a native dependency)"
  "needs-human|fbca04|Requires a person; an agent must not proceed alone"
  "deferred|cfd3d7|Could proceed; we chose not to schedule it until a condition stated in the body"
)

# Stock labels this taxonomy makes redundant. Reported, never deleted.
REDUNDANT=(bug enhancement documentation question duplicate invalid wontfix idea chore
           consider shaping agent-task meta program design-upstream design-feedback
           user-feedback "priority: medium")

seed_labels() {
  local repo="$1"
  echo "== labels: $ORG/$repo =="

  local n
  n="$(gh issue list -R "$ORG/$repo" --state all --limit 1 --json number --jq 'length' 2>/dev/null || echo 0)"
  if [[ "$n" == "0" && $FORCE -eq 0 ]]; then
    echo "  - no issues ever filed here — skipped (--force to seed anyway)"; echo; return
  fi

  local existing
  if ! existing="$(gh label list -R "$ORG/$repo" --limit 200 --json name --jq '.[].name' 2>/dev/null)"; then
    echo "  ! cannot read labels (missing repo or permission) — skipped"; echo; return
  fi

  for spec in "${LABELS[@]}"; do
    IFS='|' read -r name color desc <<< "$spec"
    if grep -qxF "$name" <<< "$existing"; then
      echo "  = $name (exists)"
    else
      run "$name" gh label create "$name" -R "$ORG/$repo" -c "$color" -d "$desc"
    fi
  done

  local found=()
  for r in "${REDUNDANT[@]}"; do
    grep -qxF "$r" <<< "$existing" && found+=("$r")
  done
  if [[ ${#found[@]} -gt 0 ]]; then
    echo "  ─ now redundant, NOT deleted: ${found[*]}"
    echo "    migrate the issues carrying them first (see migration/legacy-mapping.md),"
    echo "    then remove by hand once each is at zero uses."
  fi
  echo
}

# ----------------------------------------------------------------------- main

[[ $LABELS_ONLY -eq 0 ]] && seed_types
if [[ $TYPES_ONLY -eq 0 ]]; then
  for repo in "${REPOS[@]}"; do seed_labels "$repo"; done
fi

cat <<'EOF'
Notes
  · Issue types are org-wide — seed them once, not per repo.
  · No `area:` label is seeded. They are deliberately repo-local — add them
    by hand, and only when three or more issues would carry one.
  · No label is ever deleted by this script, and no existing issue is touched.
    Migrating existing issues is a separate, explicitly approved action.
EOF
