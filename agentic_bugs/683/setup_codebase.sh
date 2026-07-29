#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/mem0ai/mem0 codebase
git -C codebase checkout 90f2d24e832302c97e0daa55454b29657e742c15
# then: bash setup_env.sh && bash run_repro.sh
