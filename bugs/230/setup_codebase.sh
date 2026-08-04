#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/optuna/optuna codebase
git -C codebase checkout 7128a9468af453f7e0120759a35cc82918781cc4
# then: bash setup_env.sh && bash run_repro.sh
