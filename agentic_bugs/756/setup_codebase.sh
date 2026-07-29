#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 29a7b7079866d9e87bf9a71fb31686c4be674941
# then: bash setup_env.sh && bash run_repro.sh
