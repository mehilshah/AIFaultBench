#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 4f484c50b83d2f7bc779b23a37cd851409324e78
# then: bash setup_env.sh && bash run_repro.sh
