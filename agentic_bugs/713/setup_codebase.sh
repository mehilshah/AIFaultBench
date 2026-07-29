#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langflow-ai/langflow codebase
git -C codebase checkout 737d2c7a61f01ccc5724970abaf687dfeb114bbb
# then: bash setup_env.sh && bash run_repro.sh
