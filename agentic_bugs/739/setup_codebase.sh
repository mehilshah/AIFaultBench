#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Arize-ai/phoenix codebase
git -C codebase checkout 031975ccbe60e50967d8f192b6dfe6ca6de1daa7
# then: bash setup_env.sh && bash run_repro.sh
