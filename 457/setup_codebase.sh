#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout dd5926a54ee2e346f51e01afb8c0ecbb17b87a37
# then: bash setup_env.sh && bash run_repro.sh
