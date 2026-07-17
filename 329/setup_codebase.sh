#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 76ff9c2ce18c8cebf52122b57e2aeadce9793d10
# then: bash setup_env.sh && bash run_repro.sh
