#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/unslothai/unsloth codebase
git -C codebase checkout 69a6475
# then: bash setup_env.sh && bash run_repro.sh
