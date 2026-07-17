#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout e4afd05425bc5a6a74e1b1163cdeacd2e7437174
# then: bash setup_env.sh && bash run_repro.sh
