#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout b3176eff49574057d91445e23a0d2f50706f05de
# then: bash setup_env.sh && bash run_repro.sh
