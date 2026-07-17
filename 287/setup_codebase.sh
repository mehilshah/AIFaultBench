#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout a7811998498f9d1a8f869af7dab04a46e4ba2c65
# then: bash setup_env.sh && bash run_repro.sh
