#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout e12b2d6534b5fb1c0e6bdc8f486986433e502d1a
# then: bash setup_env.sh && bash run_repro.sh
