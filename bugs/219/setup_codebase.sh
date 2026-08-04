#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/datasets codebase
git -C codebase checkout 49344e52e0974f6c94abd9d6c6f35129b90b5f37
# then: bash setup_env.sh && bash run_repro.sh
