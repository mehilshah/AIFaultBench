#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout 2612e4a90e77ce3ea650546ac99a91e8c6ac9aad
# then: bash setup_env.sh && bash run_repro.sh
