#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kornia/kornia codebase
git -C codebase checkout 4bd1bd172d27ae0ffb5a811b7338150b65f404dc
# then: bash setup_env.sh && bash run_repro.sh
