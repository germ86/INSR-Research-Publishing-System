#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

case "${1:---all}" in
  --static-only) ./tests/run-tests.sh --static-only ;;
  --compile) ./tests/run-tests.sh --require-tex ;;
  --all) ./tests/run-tests.sh ;;
  *) echo "Usage: scripts/test.sh [--static-only|--compile|--all]" >&2; exit 2 ;;
esac
