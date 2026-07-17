#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/triton-inference-server/server codebase
git -C codebase checkout 441d7cf
# then: bash setup_env.sh && bash run_repro.sh
