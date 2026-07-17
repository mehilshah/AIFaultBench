#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 1ab39939d3ef44afa816b1bec4a84c957ad990f2
# then: bash setup_env.sh && bash run_repro.sh
