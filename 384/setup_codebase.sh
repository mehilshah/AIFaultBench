#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout 2ca36e3cbfb2c84c18502221564b629f3877e8be
# then: bash setup_env.sh && bash run_repro.sh
