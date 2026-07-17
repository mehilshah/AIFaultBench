#!/usr/bin/env bash
set -euo pipefail

bash setup_env.sh
docker run --rm -v "$(pwd)":/work -w /work repro-repro-063 python repro.py
