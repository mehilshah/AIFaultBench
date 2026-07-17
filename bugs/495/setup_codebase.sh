#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout bfbe99faac5f8eaed689bde7683a377594cf4023
# then: bash setup_env.sh && bash run_repro.sh
