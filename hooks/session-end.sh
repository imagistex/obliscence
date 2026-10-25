#!/usr/bin/env bash
# Perverse Experience Boundary: metadata only. The agent owns the rite.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START="${CLAUDE_PROJECT_DIR:-$PWD}"
python3 -I "$HERE/../scripts/obliscence" --vault-from "$START" --session-end --event-input >/dev/null || true
exit 0
