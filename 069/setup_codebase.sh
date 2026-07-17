#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout 88f51034b4e9f473e5d45247fc06fdc95108f7ec
# then: bash setup_env.sh && bash run_repro.sh
