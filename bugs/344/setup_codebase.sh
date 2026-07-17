#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 125202736759d37ec1bc1ce8f4de67d6ddc9c8b0
# then: bash setup_env.sh && bash run_repro.sh
