#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langflow-ai/langflow codebase
git -C codebase checkout 38eed35ffb70bda2f9ee02b84eaa311d537ae5ae
# then: bash setup_env.sh && bash run_repro.sh
