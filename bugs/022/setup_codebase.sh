#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 5d10b3bca66a2a1acc01099ba6af420ca77fd7be
# then: bash setup_env.sh && bash run_repro.sh
