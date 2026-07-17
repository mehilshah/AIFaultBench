#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout e6ab6bc3c6f40b5a9600051309eb5b1933845501
# then: bash setup_env.sh && bash run_repro.sh
