#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout 3648974a8a88221a4e3ec7edf59260908c06a353
# then: bash setup_env.sh && bash run_repro.sh
