#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 9f43bbd8e7b52135f27e8071ce3b6d517d4545fd
# then: bash setup_env.sh && bash run_repro.sh
