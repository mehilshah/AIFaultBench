#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 0ccb2bb6746bd8c5294ea9dd4761d72c8d7f48e7
# then: bash setup_env.sh && bash run_repro.sh
