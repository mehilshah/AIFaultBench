#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 41add3410424cc33d748a7fd3409132d2f6b4ad2
# then: bash setup_env.sh && bash run_repro.sh
