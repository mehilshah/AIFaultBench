#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/rotary-embedding-torch codebase
git -C codebase checkout 2da4a529854ba272535e40193177ee906ce1961b
# then: bash setup_env.sh && bash run_repro.sh
