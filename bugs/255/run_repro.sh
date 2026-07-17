#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/repro.py" >"$DIR/repro_stdout.log" 2>"$DIR/repro_stderr.log"
