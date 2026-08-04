#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/DLR-RM/stable-baselines3 codebase
git -C codebase checkout 7883ed4d20bc9edf3a22a053c77b3146c518a937
# then: bash setup_env.sh && bash run_repro.sh
