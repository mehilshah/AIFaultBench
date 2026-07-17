#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout e44f14d7d2f557b9f3add82ee4f1ed2beefbb30d
# then: bash setup_env.sh && bash run_repro.sh
