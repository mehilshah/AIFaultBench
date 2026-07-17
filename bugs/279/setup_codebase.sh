#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 1b836b1d6edc142b389de94913fdf2c3d3acfa54
# then: bash setup_env.sh && bash run_repro.sh
