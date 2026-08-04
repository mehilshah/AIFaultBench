#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kornia/kornia codebase
git -C codebase checkout 58cc4deef12892e6b3e674455c799dfa2d20d05c
# then: bash setup_env.sh && bash run_repro.sh
