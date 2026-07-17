#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run --rm \
  -v "$DIR":/workspace \
  -w /workspace \
  python:3.8-slim \
  bash -lc 'bash ./setup_env.sh && python repro.py'
