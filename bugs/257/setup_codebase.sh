#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 0173c776c3114b1d1a067adc358f09f109326a58
# then: bash setup_env.sh && bash run_repro.sh
