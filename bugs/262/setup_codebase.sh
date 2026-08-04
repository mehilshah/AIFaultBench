#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorly/tensorly codebase
git -C codebase checkout 3912bb9914a86cddbf21327ee387a9401c94dfbf
# then: bash setup_env.sh && bash run_repro.sh
