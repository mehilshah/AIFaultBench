#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

bash setup_env.sh

docker run --rm --network none -e PYTHONUNBUFFERED=1 -v "$(pwd):/work" -w /work repro-064-repro \
  > repro_stdout.log 2> repro_stderr.log
