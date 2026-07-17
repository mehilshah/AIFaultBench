#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/marimo-team/marimo codebase
git -C codebase checkout 62cd22c
# then: bash setup_env.sh && bash run_repro.sh
