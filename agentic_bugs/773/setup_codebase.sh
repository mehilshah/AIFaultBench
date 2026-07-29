#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/browser-use/browser-use codebase
git -C codebase checkout bf7775dc85e117612e66d8504c28384abecf3b6c
# then: bash setup_env.sh && bash run_repro.sh
