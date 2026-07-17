#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout d568375e5bd50e4e5fd5e4c011e7be5982ecd528
# then: bash setup_env.sh && bash run_repro.sh
