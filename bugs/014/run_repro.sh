#!/usr/bin/env bash
set -u

cd "$(dirname "$0")"
if [ -x .venv/bin/python ]; then
  PYTHON=.venv/bin/python
else
  bash setup_env.sh
  PYTHON=.venv/bin/python
fi

"$PYTHON" repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
exit "$status"
