#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! docker image inspect bug065-repro >/dev/null 2>&1; then
  docker build -t bug065-repro "${script_dir}"
fi
docker run --rm bug065-repro
