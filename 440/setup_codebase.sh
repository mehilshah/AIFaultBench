#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout b1059b73aab9043b118ff19b0cf96263ea86248a
# then: bash setup_env.sh && bash run_repro.sh
