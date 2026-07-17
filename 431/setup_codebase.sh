#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 7c574997e9027edce53820b5f38134fb3e5d05c0
# then: bash setup_env.sh && bash run_repro.sh
