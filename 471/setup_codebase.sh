#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout 2ac32f9d5a21154484a3bb2d4ab7c94c18c08119
# then: bash setup_env.sh && bash run_repro.sh
