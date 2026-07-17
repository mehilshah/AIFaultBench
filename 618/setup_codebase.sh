#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 049106473fd32f00d2b551ef61864801792acc2c
# then: bash setup_env.sh && bash run_repro.sh
