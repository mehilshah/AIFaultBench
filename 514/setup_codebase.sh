#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 816e4aef49c3f30186d65a007480bb5d4a94d17f
# then: bash setup_env.sh && bash run_repro.sh
