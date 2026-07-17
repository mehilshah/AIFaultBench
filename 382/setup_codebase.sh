#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout bbaafc2feff22ba696b517773a96c24443de3678
# then: bash setup_env.sh && bash run_repro.sh
