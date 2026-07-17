#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 5373a88000d8017e269277662cd8e93a814c66e1
# then: bash setup_env.sh && bash run_repro.sh
