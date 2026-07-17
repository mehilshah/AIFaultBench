#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/labmlai/annotated_deep_learning_paper_implementations codebase
git -C codebase checkout 999f2036a5a7c54403352211b5d1cc0df42b83f6
# then: bash setup_env.sh && bash run_repro.sh
