#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout e2f2e9e21d6723efc4c4e16e5e070dbc7e76a676
# then: bash setup_env.sh && bash run_repro.sh
