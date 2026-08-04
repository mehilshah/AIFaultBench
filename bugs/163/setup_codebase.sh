#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-cv codebase
git -C codebase checkout 9dd547a725c081db0264023717f43d14301ea3d2
# then: bash setup_env.sh && bash run_repro.sh
