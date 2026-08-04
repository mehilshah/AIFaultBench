#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kornia/kornia codebase
git -C codebase checkout bbf4b5938f33cd4ad491049d33bb714311560f6c
# then: bash setup_env.sh && bash run_repro.sh
