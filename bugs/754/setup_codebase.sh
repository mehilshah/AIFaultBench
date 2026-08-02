#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout 65ec78efddec0de3267a510b33108100faa053e4
# then: bash setup_env.sh && bash run_repro.sh
