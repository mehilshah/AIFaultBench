#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lark-parser/lark codebase
git -C codebase checkout 53c396426693a6fecab886e3c3927cdda533990f
# then: bash setup_env.sh && bash run_repro.sh
