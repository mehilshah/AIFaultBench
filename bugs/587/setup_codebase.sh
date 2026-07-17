#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/vllm-project/vllm codebase
git -C codebase checkout 3483240b7ea3d4372b6c79369ea36617f8b1fbb2
# then: bash setup_env.sh && bash run_repro.sh
