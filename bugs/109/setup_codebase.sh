#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/adapter-hub/adapters codebase
git -C codebase checkout 326d071c4dc41ab05f2a0f520813e9f4f5032979
# then: bash setup_env.sh && bash run_repro.sh
