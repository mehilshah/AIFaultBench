#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 69193c895fe721fb45e63985bb79e8d130ee7782
# then: bash setup_env.sh && bash run_repro.sh
