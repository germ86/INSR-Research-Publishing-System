#!/usr/bin/env bash
set -euo pipefail
case "${1:---all}" in
  --static-only) ./tests/run-tests.sh --static-only ;;
  --compile|--all) ./tests/run-tests.sh ;;
  *) echo "Usage: scripts/test.sh [--static-only|--compile|--all]" >&2; exit 2 ;;
esac
