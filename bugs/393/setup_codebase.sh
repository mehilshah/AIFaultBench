#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 665d5180fcc01d5700f7a9aa3f9bdb75c6055dce
# then: bash setup_env.sh && bash run_repro.sh
