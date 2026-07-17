#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/accelerate codebase
git -C codebase checkout 3533e2b0b167238fcdd3c636dcf6c3c6de983efa
# then: bash setup_env.sh && bash run_repro.sh
