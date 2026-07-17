#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout 1f84ebbf5af96eae71e2c0476d49e9cbdc5b190f
# then: bash setup_env.sh && bash run_repro.sh
