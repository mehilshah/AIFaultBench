#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lark-parser/lark codebase
git -C codebase checkout 501689455b00ff643b7901994dcb6d2a92d4412e
# then: bash setup_env.sh && bash run_repro.sh
