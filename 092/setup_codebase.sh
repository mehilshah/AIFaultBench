#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/x-transformers codebase
git -C codebase checkout 02b0190aa21ceb7688baa4bd40e6a4a3b9880446
# then: bash setup_env.sh && bash run_repro.sh
