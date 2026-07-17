#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout 3c4465806eef2129a4d7a09ed43ea451aa9c03f8
# then: bash setup_env.sh && bash run_repro.sh
