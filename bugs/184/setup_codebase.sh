#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/ludwig-ai/ludwig codebase
git -C codebase checkout 05a1a60cf970ea20f8b02d5cdbac76a168b4bd4d
# then: bash setup_env.sh && bash run_repro.sh
