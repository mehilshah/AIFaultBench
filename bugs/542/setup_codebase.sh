#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout eb93eda9fbe95cf21c1501db8b064f66b040bf33
# then: bash setup_env.sh && bash run_repro.sh
