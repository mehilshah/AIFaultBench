#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/openai/openai-agents-python codebase
git -C codebase checkout bc3607bae44d9d56c7ae0e40323d0b4a560aa254
# then: bash setup_env.sh && bash run_repro.sh
