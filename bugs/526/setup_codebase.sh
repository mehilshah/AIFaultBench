#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout df00d61d31d02465577cbbe8046af449e7685e07
# then: bash setup_env.sh && bash run_repro.sh
