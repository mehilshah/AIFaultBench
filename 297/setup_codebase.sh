#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout b783d593d4a63472a1f67d95855d54dcd75a74f8
# then: bash setup_env.sh && bash run_repro.sh
