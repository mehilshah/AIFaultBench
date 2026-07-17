#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 05212b82d764d1c4ca06e36b3220ce9c401882da
# then: bash setup_env.sh && bash run_repro.sh
