#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

stdout_file="repro_stdout.log"
stderr_file="repro_stderr.log"
tmp_stdout="$(mktemp)"
tmp_stderr="$(mktemp)"

./setup_env.sh

set +e
python3 repro.py >"$tmp_stdout" 2>"$tmp_stderr"
status=$?
set -e

cat "$tmp_stdout" | tee "$stdout_file"
cat "$tmp_stderr" | tee "$stderr_file" >&2
printf 'repro exit code: %s\n' "$status" | tee -a "$stderr_file" >&2

rm -f "$tmp_stdout" "$tmp_stderr"
exit "$status"
