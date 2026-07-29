#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/agno-agi/agno codebase
git -C codebase checkout eca49700e3d7e9ef78840abc6c15bbf5dca3f9e2
# then: bash setup_env.sh && bash run_repro.sh
