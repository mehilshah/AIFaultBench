#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langflow-ai/langflow codebase
git -C codebase checkout 0a8ef930283447d6411b71ebf3df3c627ea5e8a8
# then: bash setup_env.sh && bash run_repro.sh
