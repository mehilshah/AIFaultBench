#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 62357f218f72cce88b8e086cc372b15c119b590b
# then: bash setup_env.sh && bash run_repro.sh
