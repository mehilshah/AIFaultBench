#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/google/deepvariant codebase
git -C codebase checkout 64da16d053b49830d56370af67d6303d7df7ed4d
# then: bash setup_env.sh && bash run_repro.sh
