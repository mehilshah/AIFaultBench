#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout 33f7ba4e3c5e20c6b1a26cae354fa39900e6ffb4
# then: bash setup_env.sh && bash run_repro.sh
