#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout abae3ae4aaa6e9f5beb908b3b2f734cb12b38a9b
# then: bash setup_env.sh && bash run_repro.sh
