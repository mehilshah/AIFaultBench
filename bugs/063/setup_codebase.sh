#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout aaefb6d40b4da79b3450e5cbf65155cbea49434b
# then: bash setup_env.sh && bash run_repro.sh
