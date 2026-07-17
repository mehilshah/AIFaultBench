#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 471d2e8d6ecec261a12287c337de3e5071a9b33f
# then: bash setup_env.sh && bash run_repro.sh
