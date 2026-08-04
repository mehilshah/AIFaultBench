#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 171e079edc52bc91c6f485fed2d54a77b9798683
# then: bash setup_env.sh && bash run_repro.sh
