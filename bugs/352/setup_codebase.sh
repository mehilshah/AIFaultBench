#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout 52684952136b3dcc1120834f8af2d8f5aaa1c16a
# then: bash setup_env.sh && bash run_repro.sh
