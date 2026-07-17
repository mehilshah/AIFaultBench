#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout fe6b1cc4e80ae0396e2e404c16e6b6968ad5437e
# then: bash setup_env.sh && bash run_repro.sh
