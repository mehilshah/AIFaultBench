#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout 1ec391520aeebe580b0340fcb795cda30d08ef70
# then: bash setup_env.sh && bash run_repro.sh
