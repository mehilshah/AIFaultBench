#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 5315290b55ea9babd95a281a27c51d87b89d7c85
# then: bash setup_env.sh && bash run_repro.sh
