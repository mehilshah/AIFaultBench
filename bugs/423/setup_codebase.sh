#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 7d24bdefb5b3252505151d8c1ac0efbed3574857
# then: bash setup_env.sh && bash run_repro.sh
