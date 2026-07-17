#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 4363936534ef47721b84a95bfdc758f056c3ee98
# then: bash setup_env.sh && bash run_repro.sh
