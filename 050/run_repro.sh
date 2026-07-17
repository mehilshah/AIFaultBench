#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate
python repro.py > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)
