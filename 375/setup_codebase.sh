#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout faf677af0abec7ea25c7a33831fcabf30a795796
# then: bash setup_env.sh && bash run_repro.sh
