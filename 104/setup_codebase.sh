#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vector-quantize-pytorch codebase
git -C codebase checkout 54d29e8fba72443a29928e9f94ee52ca43eeb60a
# then: bash setup_env.sh && bash run_repro.sh
