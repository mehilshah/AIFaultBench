#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 20cfce004a79e026e7ba01d2f103b05e2637c6e0
# then: bash setup_env.sh && bash run_repro.sh
