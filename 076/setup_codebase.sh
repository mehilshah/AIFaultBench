#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/matterport/Mask_RCNN codebase
git -C codebase checkout 3deaec5d902d16e1daf56b62d5971d428dc920bc
# then: bash setup_env.sh && bash run_repro.sh
