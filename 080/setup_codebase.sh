#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vit-pytorch codebase
git -C codebase checkout 90be7233a3f55c29692a72da6ee4dcb5aab267d4
# then: bash setup_env.sh && bash run_repro.sh
