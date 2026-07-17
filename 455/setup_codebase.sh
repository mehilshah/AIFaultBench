#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout cc82b674b5db38b9a393463d38afe66e8f48ac1c
# then: bash setup_env.sh && bash run_repro.sh
