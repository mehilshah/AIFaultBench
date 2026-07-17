#!/usr/bin/env bash
set -uo pipefail

python3 repro.py > repro_stdout.log 2> repro_stderr.log
status=$?

printf 'repro exit status: %s\n' "$status"
exit 0
