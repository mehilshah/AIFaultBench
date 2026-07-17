#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout bb44e10a93d3c136760d6d31d387f600429e1c61
# then: bash setup_env.sh && bash run_repro.sh
