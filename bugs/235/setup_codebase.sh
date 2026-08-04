#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/equinox codebase
git -C codebase checkout 028a6f466da7aa99e73a92a3549f632b51d95e34
# then: bash setup_env.sh && bash run_repro.sh
