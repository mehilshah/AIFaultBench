#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 900881a24749fd788b64559aff64921954967d29
# then: bash setup_env.sh && bash run_repro.sh
