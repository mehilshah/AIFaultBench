#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout fed2253c4a807e85ba61887efd0bb10ee869d094
# then: bash setup_env.sh && bash run_repro.sh
