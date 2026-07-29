#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout 31a502c4fa1c6aae0acb52448b730732678847da
# then: bash setup_env.sh && bash run_repro.sh
