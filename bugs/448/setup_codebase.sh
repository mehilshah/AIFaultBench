#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 48f94e65d54b20e86ac68872622f239a89aa33fe
# then: bash setup_env.sh && bash run_repro.sh
