#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
: > repro_stdout.log
: > repro_stderr.log

python3 repro.py > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)

