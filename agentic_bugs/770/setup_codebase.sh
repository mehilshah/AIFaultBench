#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout f3c122810a8a2065f24dcd306dfdd46e5d3fcd0d
# then: bash setup_env.sh && bash run_repro.sh
