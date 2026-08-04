#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/clearml/clearml codebase
git -C codebase checkout 7d882ddc46053e142e5c28f5ebde007e0b7523e2
# then: bash setup_env.sh && bash run_repro.sh
