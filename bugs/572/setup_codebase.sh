#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout c3ea690d48c90599f83c6a305040d06c98e58a50
# then: bash setup_env.sh && bash run_repro.sh
