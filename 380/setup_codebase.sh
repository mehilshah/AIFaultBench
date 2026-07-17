#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout a41a96b19f2b5e75567c85ff9155e4bb09c8e539
# then: bash setup_env.sh && bash run_repro.sh
