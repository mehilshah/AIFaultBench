#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lark-parser/lark codebase
git -C codebase checkout 44483c91b7651bb6f9672c015c408beb4afdbb72
# then: bash setup_env.sh && bash run_repro.sh
