#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 0a0f0610a4d223a258cd73e65abe852a8f703226
# then: bash setup_env.sh && bash run_repro.sh
