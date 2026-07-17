#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vit-pytorch codebase
git -C codebase checkout ce4bcd08fbab864e92167415552a722ff5ce2005
# then: bash setup_env.sh && bash run_repro.sh
