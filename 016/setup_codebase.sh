#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout abb7ed6a4628118042876c17ba48c559e0fb5025
# then: bash setup_env.sh && bash run_repro.sh
