#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout c41a3c3ed8ab16d4fadd2f08ee0f49cb78e79994
# then: bash setup_env.sh && bash run_repro.sh
