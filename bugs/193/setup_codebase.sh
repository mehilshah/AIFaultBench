#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/equinox codebase
git -C codebase checkout 09e19a6fad5bae0c1091c6f5aaba6ef7b91a149e
# then: bash setup_env.sh && bash run_repro.sh
