#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 1244df91a41dae7100975d6e4db8253a72b29b66
# then: bash setup_env.sh && bash run_repro.sh
