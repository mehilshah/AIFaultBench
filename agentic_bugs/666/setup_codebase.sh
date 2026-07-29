#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout 5c684c18df01895832ed0e0caecb6896f72890da
# then: bash setup_env.sh && bash run_repro.sh
