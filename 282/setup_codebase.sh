#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 3147de52286b807368fd9429844e50e16d8d7cc7
# then: bash setup_env.sh && bash run_repro.sh
