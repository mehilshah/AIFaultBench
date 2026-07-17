#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# DeepSpeed Team
set -u

cd "$(dirname "$0")"

PYTHON_BIN=".venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

"$PYTHON_BIN" repro.py > repro_stdout.log 2> repro_stderr.log
status=$?

printf 'exit_code=%s\n' "$status" >> repro_stdout.log
exit "$status"
