#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout ab7961a14a59be9a0170f1654315d5c2be44c015
# then: bash setup_env.sh && bash run_repro.sh
