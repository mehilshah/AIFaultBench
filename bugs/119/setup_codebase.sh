#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/cornellius-gp/gpytorch codebase
git -C codebase checkout d501c284d05a1186868dc3fb20e0fa6ad32d32ac
# then: bash setup_env.sh && bash run_repro.sh
