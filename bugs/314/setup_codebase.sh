#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 6d9a2a2a2fc6a586404ee29ea665bc5b2adfa13f
# then: bash setup_env.sh && bash run_repro.sh
