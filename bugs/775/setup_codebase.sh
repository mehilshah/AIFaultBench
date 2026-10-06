#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lark-parser/lark codebase
git -C codebase checkout 9a4fb9c7458e8155636773a3cded0016d52516da
# then: bash setup_env.sh && bash run_repro.sh
