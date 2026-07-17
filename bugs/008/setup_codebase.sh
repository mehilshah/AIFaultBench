#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 5c0617a8f3041bfa97db45748050b9c254cb95d6
# then: bash setup_env.sh && bash run_repro.sh
