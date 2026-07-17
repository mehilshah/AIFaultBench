#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 4250605d1e353e8f3e5f943abc485d5bbe1fb250
# then: bash setup_env.sh && bash run_repro.sh
