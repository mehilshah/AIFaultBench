#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 5130530c6eda2fbe971e1d3cef83dc474af11c6e
# then: bash setup_env.sh && bash run_repro.sh
