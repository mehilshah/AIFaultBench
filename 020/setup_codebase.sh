#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 631e763896a7cc4be6edf20c659938e02715fee8
# then: bash setup_env.sh && bash run_repro.sh
