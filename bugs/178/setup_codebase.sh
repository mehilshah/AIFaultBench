#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lark-parser/lark codebase
git -C codebase checkout f79772cd4c6d2076b5dc01f399dbb816cc484f77
# then: bash setup_env.sh && bash run_repro.sh
