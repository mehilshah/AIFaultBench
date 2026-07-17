#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 535ed7ad76113cc2fedaf4b230aabedbb348108f
# then: bash setup_env.sh && bash run_repro.sh
