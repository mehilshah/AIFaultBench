#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout 6f8f50b4b8d722d67b7da03fa3e75344f3f03a9f
# then: bash setup_env.sh && bash run_repro.sh
