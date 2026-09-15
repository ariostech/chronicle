#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${BASE_SHA:-}" || -z "${HEAD_SHA:-}" ]]; then
  echo "BASE_SHA and HEAD_SHA are required." >&2
  exit 2
fi

mapfile -t commits < <(git rev-list --no-merges "${BASE_SHA}..${HEAD_SHA}")

if [[ ${#commits[@]} -eq 0 ]]; then
  echo "No pull-request commits found."
  exit 0
fi

missing=0

for commit in "${commits[@]}"; do
  if ! git show -s --format=%B "$commit" | grep -Eq '^Signed-off-by: .+ <[^<>[:space:]]+@[^<>[:space:]]+>$'; then
    echo "Missing valid DCO sign-off: $commit" >&2
    missing=1
  fi
done

if [[ $missing -ne 0 ]]; then
  echo >&2
  echo "Add a sign-off with 'git commit -s' and update the pull request." >&2
  exit 1
fi

echo "All pull-request commits contain a DCO sign-off."
