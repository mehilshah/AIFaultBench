#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/jaxtyping codebase
git -C codebase checkout fe61644be8590cf0a89bacc278283e1e4b9ea3e4
# then: bash setup_env.sh && bash run_repro.sh
