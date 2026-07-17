#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout 41d475b75a230221e21d9cac5d69655e3415e3a4
# then: bash setup_env.sh && bash run_repro.sh
