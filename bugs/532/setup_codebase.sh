#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 6382a3db4dd1e129ce8be68649db6fcbae015e8c
# then: bash setup_env.sh && bash run_repro.sh
