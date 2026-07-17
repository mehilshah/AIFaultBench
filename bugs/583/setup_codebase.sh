#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 5bd51bd189ab217e6e0ae708dceeb429689c00f7
# then: bash setup_env.sh && bash run_repro.sh
