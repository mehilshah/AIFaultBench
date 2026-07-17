#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 8a9369d03e800e413a31503ceb0e5d39e390d845
# then: bash setup_env.sh && bash run_repro.sh
