#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/towhee-io/towhee codebase
git -C codebase checkout fe856301680713032e9613cf2500932f0ae3ad13
# then: bash setup_env.sh && bash run_repro.sh
