#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/deepspeedai/DeepSpeedExamples codebase
git -C codebase checkout be0a0e189714f7e4cb523cb8d40ced1da964153a
# then: bash setup_env.sh && bash run_repro.sh
