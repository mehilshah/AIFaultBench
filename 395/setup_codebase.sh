#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout b4cfbc24d33ca17bc764a75ffe749654654521c1
# then: bash setup_env.sh && bash run_repro.sh
