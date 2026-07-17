#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout 131518c15cef20aa6cfe3c6831af3a1d0637e3d1
# then: bash setup_env.sh && bash run_repro.sh
