#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 5f0f949de9667552d85f0922191a05a0c9d0a99c
# then: bash setup_env.sh && bash run_repro.sh
