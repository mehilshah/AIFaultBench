#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout fafadc532351f3434f4d4abd4b61d356932607d8
# then: bash setup_env.sh && bash run_repro.sh
