#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/ao codebase
git -C codebase checkout ff6d9e24421cf4b1e98a2ae139144adbc038e6f8
# then: bash setup_env.sh && bash run_repro.sh
