#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/browser-use/browser-use codebase
git -C codebase checkout a1870b8b969553c375755c77d5d1cebf477c51f6
# then: bash setup_env.sh && bash run_repro.sh
