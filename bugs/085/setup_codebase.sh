#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vit-pytorch codebase
git -C codebase checkout 46dcaf23d8a044a41e1909ab8cfcf815c0589d65
# then: bash setup_env.sh && bash run_repro.sh
