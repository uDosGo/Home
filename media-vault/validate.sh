#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/media}"
REQUIRED=(movies tv music home-videos playlists)

missing=0
for d in "${REQUIRED[@]}"; do
  if [[ ! -d "$ROOT/$d" ]]; then
    echo "missing: $ROOT/$d"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "media vault validation failed"
  exit 1
fi

echo "media vault validation passed: $ROOT"
