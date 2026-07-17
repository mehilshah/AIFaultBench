#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 085710a88cfdcc1a8bbfa4b1ba1bc6cceb63e8c9
# then: bash setup_env.sh && bash run_repro.sh
