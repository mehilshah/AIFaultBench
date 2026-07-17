#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vit-pytorch codebase
git -C codebase checkout 8208c859a5474b2d93b429202833fcd9f395ec30
# then: bash setup_env.sh && bash run_repro.sh
