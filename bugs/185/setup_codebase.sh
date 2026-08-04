#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/marimo-team/marimo codebase
git -C codebase checkout 371f3c856a1ecc54f14e21cfe3078351a5fc949d
# then: bash setup_env.sh && bash run_repro.sh
