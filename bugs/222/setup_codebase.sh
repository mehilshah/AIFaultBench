#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/towhee-io/towhee codebase
git -C codebase checkout fe85630
# then: bash setup_env.sh && bash run_repro.sh
