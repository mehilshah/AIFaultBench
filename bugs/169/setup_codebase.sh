#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kornia/kornia codebase
git -C codebase checkout 30eec3671883738f827da877fce2257f3b1be192
# then: bash setup_env.sh && bash run_repro.sh
