#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout f4f5503bfa0db535cb505c2653b9f087a2dabc9d
# then: bash setup_env.sh && bash run_repro.sh
