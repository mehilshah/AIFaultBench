#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 30a6a3435fc49ee7185d5e14d2abff6854c48b4d
# then: bash setup_env.sh && bash run_repro.sh
