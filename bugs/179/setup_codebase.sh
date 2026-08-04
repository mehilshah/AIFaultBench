#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lark-parser/lark codebase
git -C codebase checkout 9379161aad48994302251803ef7e932cbbd3c4ba
# then: bash setup_env.sh && bash run_repro.sh
