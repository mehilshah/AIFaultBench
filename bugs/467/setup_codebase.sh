#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 901ab69a1601ba1a7c63523356c5acb1d66b7ea9
# then: bash setup_env.sh && bash run_repro.sh
