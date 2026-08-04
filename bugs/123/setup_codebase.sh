#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/DLR-RM/stable-baselines3 codebase
git -C codebase checkout d35597f21f75bcd04e7ad155b1522d0a28f884ff
# then: bash setup_env.sh && bash run_repro.sh
