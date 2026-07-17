#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/jax-ml/jax codebase
git -C codebase checkout 6a19c8b5ae8986e3aba44cb78b4bb024cd1997b2
# then: bash setup_env.sh && bash run_repro.sh
