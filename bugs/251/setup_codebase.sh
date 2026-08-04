#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 57f05800e3ae631b242d60f5efd46887762d07d4
# then: bash setup_env.sh && bash run_repro.sh
