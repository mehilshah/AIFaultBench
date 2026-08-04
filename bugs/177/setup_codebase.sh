#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lark-parser/lark codebase
git -C codebase checkout 95e9700f2eb36511bfb83379d7b1186c6f2652c5
# then: bash setup_env.sh && bash run_repro.sh
