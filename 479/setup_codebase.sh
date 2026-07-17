#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 25b85c1d0b18adf0271fb9f4b547aea244a889ca
# then: bash setup_env.sh && bash run_repro.sh
