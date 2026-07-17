#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

exec > >(tee "$ROOT/repro_stdout.log") 2> >(tee "$ROOT/repro_stderr.log" >&2)

python3 repro.py
