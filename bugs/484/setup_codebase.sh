#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 3e83f4348f0c6baea8bee3d1ff7676f50e11e74c
# then: bash setup_env.sh && bash run_repro.sh
