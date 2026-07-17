#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 5b85738576fc67e7be37d66328dab839841db3ff
# then: bash setup_env.sh && bash run_repro.sh
