#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 2995df37bbc723fdffa6d91a86d143fd13dc63ce
# then: bash setup_env.sh && bash run_repro.sh
