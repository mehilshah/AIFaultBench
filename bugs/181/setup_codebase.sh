#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout dd2912a045f1a1a0c87528b41c9854fc7454d4b0
# then: bash setup_env.sh && bash run_repro.sh
