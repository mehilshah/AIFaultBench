#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/semantic-kernel codebase
git -C codebase checkout 1c11258a3242a5a9f8dfa421674fa2108c5e5456
# then: bash setup_env.sh && bash run_repro.sh
