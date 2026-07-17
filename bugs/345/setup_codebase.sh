#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 7b6de017d4ca3f405d630eb59ec6c111cf7ded4c
# then: bash setup_env.sh && bash run_repro.sh
