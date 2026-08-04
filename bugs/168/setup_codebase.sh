#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kornia/kornia codebase
git -C codebase checkout 9cea9aebe06d24154b26e61254271d55b36fbc98
# then: bash setup_env.sh && bash run_repro.sh
