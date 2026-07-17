#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/unit8co/darts codebase
git -C codebase checkout c52ec83
# then: bash setup_env.sh && bash run_repro.sh
