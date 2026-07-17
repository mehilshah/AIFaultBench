#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/detectron2 codebase
git -C codebase checkout 137745de04797fa488a2bc86955795e91318b8ee
# then: bash setup_env.sh && bash run_repro.sh
