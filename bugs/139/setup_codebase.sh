#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout 6ab2af610db6cfafa505589419894c2dd34d59fc
# then: bash setup_env.sh && bash run_repro.sh
