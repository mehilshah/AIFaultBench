#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/cornellius-gp/gpytorch codebase
git -C codebase checkout d501c28
# then: bash setup_env.sh && bash run_repro.sh
