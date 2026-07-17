#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 3fe392b63c849e22b9ce10860c0ae2c4de9b6fd1
# then: bash setup_env.sh && bash run_repro.sh
