#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout b56f87af9e968003666e61f88185a93ff0f0eee8
# then: bash setup_env.sh && bash run_repro.sh
