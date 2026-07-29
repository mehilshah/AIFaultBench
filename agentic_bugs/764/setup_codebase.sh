#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langflow-ai/langflow codebase
git -C codebase checkout 0a4dbc8c6c95d2576e180dccb04f2ae1f6ffa47f
# then: bash setup_env.sh && bash run_repro.sh
