#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 47ce5df4c625a6861d7adff7229b0a40b9230d83
# then: bash setup_env.sh && bash run_repro.sh
