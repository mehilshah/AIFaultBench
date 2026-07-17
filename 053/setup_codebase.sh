#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout 6623a072e7eef484c3defa44dc16d824eac434cb
# then: bash setup_env.sh && bash run_repro.sh
