#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 7a3a902519afb8b8d1182bee2395a26b5cfe812d
# then: bash setup_env.sh && bash run_repro.sh
