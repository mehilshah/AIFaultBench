#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/labmlai/annotated_deep_learning_paper_implementations codebase
git -C codebase checkout 05632f9f8e0de4657c210a13954a81f9556fd1ed
# then: bash setup_env.sh && bash run_repro.sh
