#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/NVIDIA-NeMo/NeMo codebase
git -C codebase checkout 0d69e53
# then: bash setup_env.sh && bash run_repro.sh
