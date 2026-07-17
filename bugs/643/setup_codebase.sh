#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 5e198f24a286017914c78efd94422bf7c2817da5
# then: bash setup_env.sh && bash run_repro.sh
