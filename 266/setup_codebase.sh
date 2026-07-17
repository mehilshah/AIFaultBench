#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 4e85fb88cdac6818d820d8f36b99427b01ec6d58
# then: bash setup_env.sh && bash run_repro.sh
