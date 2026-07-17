#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 898298dfcd112c337d44523dd1f28bb6b663c1e4
# then: bash setup_env.sh && bash run_repro.sh
