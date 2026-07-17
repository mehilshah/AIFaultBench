#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 5445446014c80f23841afddbadf551d8c2adc200
# then: bash setup_env.sh && bash run_repro.sh
