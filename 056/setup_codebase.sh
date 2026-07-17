#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout cbe83d8244cb53e0a42299b8b5da4c460c6ae768
# then: bash setup_env.sh && bash run_repro.sh
