#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Project-MONAI/MONAI codebase
git -C codebase checkout 69f3dd26ed2a65e89ae89d951bb16f2dcb4d7c5d
# then: bash setup_env.sh && bash run_repro.sh
