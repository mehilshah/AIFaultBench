#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/xformers codebase
git -C codebase checkout a2f37f8c5f4e3ae0d3459a92e42cd1aeb45b03bc
# then: bash setup_env.sh && bash run_repro.sh
