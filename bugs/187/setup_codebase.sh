#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/marimo-team/marimo codebase
git -C codebase checkout 62cd22c272df1e7fe558b7d8e919b2fc42518b5d
# then: bash setup_env.sh && bash run_repro.sh
