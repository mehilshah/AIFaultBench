#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 5063aa5566f068b68bba799b6604e9ac14eaf37c
# then: bash setup_env.sh && bash run_repro.sh
