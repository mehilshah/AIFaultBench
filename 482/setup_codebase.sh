#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout cd5f656651c3ef2c9f05fcf3345e147577d81fd8
# then: bash setup_env.sh && bash run_repro.sh
