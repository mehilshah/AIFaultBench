#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 0592fdc56f400ba6feedbf7b3b77b992ac6b06e1
# then: bash setup_env.sh && bash run_repro.sh
