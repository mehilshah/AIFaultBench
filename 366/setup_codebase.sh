#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout dd127d82ed29c40b7daf6e751add49ff371b1d9d
# then: bash setup_env.sh && bash run_repro.sh
