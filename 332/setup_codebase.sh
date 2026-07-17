#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 26ec30e8add5faec242aed6a4bfe0d23a6e9befd
# then: bash setup_env.sh && bash run_repro.sh
