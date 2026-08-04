#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/optuna/optuna codebase
git -C codebase checkout 632ab66c6b6c2b2ad09f51e58554d37c2ee3e792
# then: bash setup_env.sh && bash run_repro.sh
