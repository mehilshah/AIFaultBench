#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout 789daa2f7a487771723de298aa3d0c7d87236d42
# then: bash setup_env.sh && bash run_repro.sh
