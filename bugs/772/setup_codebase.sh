#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 503dece3fb0cfcaaf7b11fc78a76eee810ab63bf
# then: bash setup_env.sh && bash run_repro.sh
