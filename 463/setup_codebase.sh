#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 5073cd4d871bd39a04a75aef1db21e065b903f1a
# then: bash setup_env.sh && bash run_repro.sh
