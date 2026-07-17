#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout ab49b59dd37a4210f1d0102b89b7b00340217cf1
# then: bash setup_env.sh && bash run_repro.sh
