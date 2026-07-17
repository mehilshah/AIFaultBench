#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout e60a4243988a636bda8a6bf99044fb313d5a9e0e
# then: bash setup_env.sh && bash run_repro.sh
