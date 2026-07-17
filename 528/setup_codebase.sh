#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout ae6e1c01a9b4d06bbc13868071a3ec36c5ed2d33
# then: bash setup_env.sh && bash run_repro.sh
