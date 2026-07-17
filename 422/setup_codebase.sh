#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 612ab081e633861f6c7178b7e3e5eaf15b429b94
# then: bash setup_env.sh && bash run_repro.sh
