#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/mem0ai/mem0 codebase
git -C codebase checkout 8d6b7c1d671af329dbf43a984fe1b3207ef59fe7
# then: bash setup_env.sh && bash run_repro.sh
