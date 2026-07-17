#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vit-pytorch codebase
git -C codebase checkout 141239ca86afc6e1fe6f4e50b60d173e21ca38ec
# then: bash setup_env.sh && bash run_repro.sh
