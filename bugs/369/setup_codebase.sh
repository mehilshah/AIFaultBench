#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout a2648075f2e76c0fbcef89c84db2319d7b56cc17
# then: bash setup_env.sh && bash run_repro.sh
