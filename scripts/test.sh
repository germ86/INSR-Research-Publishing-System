#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

test_runner="$repo_root/tests/run-tests.sh"

case "${1:---all}" in
  --static-only) bash "$test_runner" --static-only ;;
  --compile) bash "$test_runner" --require-tex ;;
  --all) bash "$test_runner" ;;
  *) echo "Usage: scripts/test.sh [--static-only|--compile|--all]" >&2; exit 2 ;;
esac
