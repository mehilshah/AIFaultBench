#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 85cf9fc12b1138c1f2adbed8a761356c3f4197e7
# then: bash setup_env.sh && bash run_repro.sh
