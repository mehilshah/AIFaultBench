#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 67adb473a4d96652fb1b38fb2617f01eacf9481f
# then: bash setup_env.sh && bash run_repro.sh
