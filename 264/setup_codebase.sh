#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tinygrad/tinygrad codebase
git -C codebase checkout 9b4de8a
# then: bash setup_env.sh && bash run_repro.sh
