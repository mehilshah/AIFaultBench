#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/DLR-RM/stable-baselines3 codebase
git -C codebase checkout 6c00565778e5815e4589afc7499aafbd020535ae
# then: bash setup_env.sh && bash run_repro.sh
