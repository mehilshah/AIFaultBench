#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout c03f5949ad10a2b008882fce2bb2d18c80f3e725
# then: bash setup_env.sh && bash run_repro.sh
