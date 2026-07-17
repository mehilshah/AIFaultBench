#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/labmlai/annotated_deep_learning_paper_implementations codebase
git -C codebase checkout a0679ecd90b41b8e012995a6bdf095edae590b17
# then: bash setup_env.sh && bash run_repro.sh
