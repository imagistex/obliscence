#!/usr/bin/env bash
# Obverse Experience Boundary: a factual offer, never a forced close.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START="${CLAUDE_PROJECT_DIR:-$PWD}"
OUT="$(python3 -I "$HERE/../scripts/obliscence" --vault-from "$START" --hook --event-input || true)"
if [ -z "$OUT" ]; then echo '{}'; exit 0; fi
python3 -I - "$OUT" <<'PY'
import json, sys
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": sys.argv[1]}}))
PY
exit 0
