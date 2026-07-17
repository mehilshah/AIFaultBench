#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 5e89e4e7c99a3d3122387548058d4ea20baca926
# then: bash setup_env.sh && bash run_repro.sh
