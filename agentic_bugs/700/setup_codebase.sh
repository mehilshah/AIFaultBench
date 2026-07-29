#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 83ff2f7ed09788e130965349929f8bd5152e507e
# then: bash setup_env.sh && bash run_repro.sh
