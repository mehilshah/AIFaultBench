#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Lightning-AI/pytorch-lightning codebase
git -C codebase checkout 78bf0214a0ad7571391619dca952c13988c0dc51
# then: bash setup_env.sh && bash run_repro.sh
