#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/vector-quantize-pytorch codebase
git -C codebase checkout ac5d63174dd234ab75259a68a4ab246774863f6e
# then: bash setup_env.sh && bash run_repro.sh
