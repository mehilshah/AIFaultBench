#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout 818663b8b699d8a47026ac952a3adcbdd6350a67
# then: bash setup_env.sh && bash run_repro.sh
