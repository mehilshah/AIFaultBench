#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 5279767b48b562d0a26428b4b43b5383dfa895f3
# then: bash setup_env.sh && bash run_repro.sh
