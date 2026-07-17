#!/usr/bin/env bash
set -u

cd "$(dirname "$0")"

: > repro_stdout.log
: > repro_stderr.log

python3 repro.py > repro_stdout.log 2> repro_stderr.log
exit $?
