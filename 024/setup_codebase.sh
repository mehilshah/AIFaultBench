#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 2229297fa2a8ab354dbf68e6d61db99c51e57b2c
# then: bash setup_env.sh && bash run_repro.sh
