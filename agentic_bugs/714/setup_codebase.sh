#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langflow-ai/langflow codebase
git -C codebase checkout 263cfc68f170110473a9a1a47c1d0f1b629ab548
# then: bash setup_env.sh && bash run_repro.sh
