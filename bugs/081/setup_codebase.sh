#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vit-pytorch codebase
git -C codebase checkout 5578ac472faf3903d4739ba783f3875b77177e57
# then: bash setup_env.sh && bash run_repro.sh
