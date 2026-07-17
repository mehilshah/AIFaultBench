#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 262e222e5f038161866f02ec21527d66453f487d
# then: bash setup_env.sh && bash run_repro.sh
