#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/smolagents codebase
git -C codebase checkout f76dee172666d7dad178aed06b257c629967733b
# then: bash setup_env.sh && bash run_repro.sh
