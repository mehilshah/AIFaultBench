#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/DLR-RM/stable-baselines3 codebase
git -C codebase checkout f7a89e1e1d4f0c98b0564fc9ea62372ae6795adb
# then: bash setup_env.sh && bash run_repro.sh
