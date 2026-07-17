#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/pytorch-image-models codebase
git -C codebase checkout a94c10fce182362e26e128e1b51863dff2a1d558
# then: bash setup_env.sh && bash run_repro.sh
