#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/rotary-embedding-torch codebase
git -C codebase checkout 22cac59a55ae25cd06b4522d891278aedd929184
# then: bash setup_env.sh && bash run_repro.sh
