#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout eacbcdd8501527e3b9898c46f7b9758e461a9f95
# then: bash setup_env.sh && bash run_repro.sh
