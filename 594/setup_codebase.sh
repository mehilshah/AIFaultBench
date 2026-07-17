#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 58d4bf8194fbe2efe7da845cf5192d7e70f58de2
# then: bash setup_env.sh && bash run_repro.sh
