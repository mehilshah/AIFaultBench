#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/x-transformers codebase
git -C codebase checkout aa380f17b6f1e762604278ad2cd9b6ecc804f35e
# then: bash setup_env.sh && bash run_repro.sh
