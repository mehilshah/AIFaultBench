#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 52cf596100dc2d0e6d678835fe05d88dc8584fd9
# then: bash setup_env.sh && bash run_repro.sh
