#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout f3d42be118f9af7ed9697b686fba09a8bdcd71d1
# then: bash setup_env.sh && bash run_repro.sh
