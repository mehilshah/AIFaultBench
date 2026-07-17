#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 9e0bc850e9a86c0cc50866eb3cc48c3c1a505110
# then: bash setup_env.sh && bash run_repro.sh
