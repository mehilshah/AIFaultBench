#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 39f060e71832e5e40bb5138746744020afb498e7
# then: bash setup_env.sh && bash run_repro.sh
