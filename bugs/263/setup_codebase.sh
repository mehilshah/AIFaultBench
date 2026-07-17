#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/thu-ml/tianshou codebase
git -C codebase checkout be657fa
# then: bash setup_env.sh && bash run_repro.sh
