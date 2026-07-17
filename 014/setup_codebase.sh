#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 47571f3b2247b68a4370a3dd7c659d87e0affcad
# then: bash setup_env.sh && bash run_repro.sh
