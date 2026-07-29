#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/agno-agi/agno codebase
git -C codebase checkout 1a32f1651b0427ed8c70aa6123a5a93610d8c3d0
# then: bash setup_env.sh && bash run_repro.sh
