#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout 54392950c4142c96ccc0f8dfd4a9a586edbe5cf2
# then: bash setup_env.sh && bash run_repro.sh
