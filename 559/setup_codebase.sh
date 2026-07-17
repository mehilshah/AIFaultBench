#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout f054799e7fb74554591a6085ca3b920e0b10f923
# then: bash setup_env.sh && bash run_repro.sh
