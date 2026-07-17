#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout 91e6e1737efd8788c3199a93ca95016cf69918b0
# then: bash setup_env.sh && bash run_repro.sh
