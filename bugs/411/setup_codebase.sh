#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout 08cb3dde577747f6ca6638c884fd66fd16cf2e9d
# then: bash setup_env.sh && bash run_repro.sh
