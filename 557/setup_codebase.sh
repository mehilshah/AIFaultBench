#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout d773308ca726766d6d2867f1fb8732df3d1dc5a3
# then: bash setup_env.sh && bash run_repro.sh
