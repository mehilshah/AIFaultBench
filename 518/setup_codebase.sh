#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 934ba74c5e3f0bc3c07f3b8e2ad204d3fec6006e
# then: bash setup_env.sh && bash run_repro.sh
