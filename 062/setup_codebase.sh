#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout 12795962e429e758d5b97b4755b7c635bff51b9a
# then: bash setup_env.sh && bash run_repro.sh
