#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/run-llama/llama_index codebase
git -C codebase checkout c346327e51eaf26c84a495f8bee1f9ea81542bc7
# then: bash setup_env.sh && bash run_repro.sh
