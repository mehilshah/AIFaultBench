#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/protectai/modelscan codebase
git -C codebase checkout a647a2bd2ee30cd116a21154ed9413a18b3e73b8
# then: bash setup_env.sh && bash run_repro.sh
