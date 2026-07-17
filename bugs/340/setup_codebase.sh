#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 62a5fc474f255b0c78b337d9f4abf4428148c5c5
# then: bash setup_env.sh && bash run_repro.sh
