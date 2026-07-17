#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 283ce7733ec23786d41751f185093eac83c0ef8d
# then: bash setup_env.sh && bash run_repro.sh
