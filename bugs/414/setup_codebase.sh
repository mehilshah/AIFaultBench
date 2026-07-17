#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout b6326f7726429241a66c888c4d70d588049f77a9
# then: bash setup_env.sh && bash run_repro.sh
