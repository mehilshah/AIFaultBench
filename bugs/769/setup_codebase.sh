#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout d6b7191503bcab998afe3378904ae6a5dfd5f0a3
# then: bash setup_env.sh && bash run_repro.sh
