#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyg-team/pytorch_geometric codebase
git -C codebase checkout 9b794b600d41802edaad26aac18bff958fc8f642
# then: bash setup_env.sh && bash run_repro.sh
