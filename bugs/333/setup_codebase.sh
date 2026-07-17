#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 5f98958cb133c0b9e50831cc4f66ced2404c6729
# then: bash setup_env.sh && bash run_repro.sh
