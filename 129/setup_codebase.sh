#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebook/Ax codebase
git -C codebase checkout 708ace0
# then: bash setup_env.sh && bash run_repro.sh
