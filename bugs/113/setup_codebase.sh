#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/arogozhnikov/einops codebase
git -C codebase checkout 1d3f9c4
# then: bash setup_env.sh && bash run_repro.sh
