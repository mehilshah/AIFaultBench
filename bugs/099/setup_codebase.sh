#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/rotary-embedding-torch codebase
git -C codebase checkout cd0971297a26ec557ad0c65a6d9e4e1ffca8ae89
# then: bash setup_env.sh && bash run_repro.sh
