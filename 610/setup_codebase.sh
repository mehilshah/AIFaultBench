#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 2e25642a6fe33b23c524884bbf40213336d57126
# then: bash setup_env.sh && bash run_repro.sh
