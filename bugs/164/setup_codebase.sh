#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kornia/kornia codebase
git -C codebase checkout 7700ce08cb33c729d79e77225d05b333b1ec7d42
# then: bash setup_env.sh && bash run_repro.sh
