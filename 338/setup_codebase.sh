#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout ae4d1bbfefab7e4f2f49a744838a2d9c7713146d
# then: bash setup_env.sh && bash run_repro.sh
