#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 7be582697b27277e2756a3878f563fa9dfea30aa
# then: bash setup_env.sh && bash run_repro.sh
