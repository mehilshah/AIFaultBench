#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout c1c5a190b7087bd40c88594b7ef7b0f79040a761
# then: bash setup_env.sh && bash run_repro.sh
