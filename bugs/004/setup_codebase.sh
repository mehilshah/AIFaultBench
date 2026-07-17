#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 8c5c79c27c4bb2843308bf8623daa24f4f3cbe62
# then: bash setup_env.sh && bash run_repro.sh
