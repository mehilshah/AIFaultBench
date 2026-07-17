#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 71a6fd9f0df04d3764dfa999268a05d87903a85a
# then: bash setup_env.sh && bash run_repro.sh
