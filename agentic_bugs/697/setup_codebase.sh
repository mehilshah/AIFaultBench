#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 67b15aee2ba1ea70ba9536d94f0be4f1a598578c
# then: bash setup_env.sh && bash run_repro.sh
