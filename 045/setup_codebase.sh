#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/fairseq codebase
git -C codebase checkout b5d89cddc9e4a0af831d2aafc1ba7dbf0f1b10d0
# then: bash setup_env.sh && bash run_repro.sh
