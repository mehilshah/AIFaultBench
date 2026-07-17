#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vit-pytorch codebase
git -C codebase checkout 5699ed7d139062020d1394f0e85a07f706c87c09
# then: bash setup_env.sh && bash run_repro.sh
