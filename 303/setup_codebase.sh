#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 0ba235294fcbe35f5c42681bd85666dff5c48a93
# then: bash setup_env.sh && bash run_repro.sh
