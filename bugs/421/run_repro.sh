#!/usr/bin/env bash
set -u

python3 repro.py > repro_stdout.log 2> repro_stderr.log
