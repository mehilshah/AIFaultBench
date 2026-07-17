#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/x-transformers codebase
git -C codebase checkout cdf51f7127d2af478030b81c44d7a1ddb35716a8
# then: bash setup_env.sh && bash run_repro.sh
