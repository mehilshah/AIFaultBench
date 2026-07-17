#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout d2bb939a1bfba3b7a6f7d7b102a2771471657319
# then: bash setup_env.sh && bash run_repro.sh
