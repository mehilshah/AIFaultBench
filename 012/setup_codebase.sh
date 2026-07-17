#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 325e10e2602e23c8a2d33a611c6b3286372b0b1a
# then: bash setup_env.sh && bash run_repro.sh
