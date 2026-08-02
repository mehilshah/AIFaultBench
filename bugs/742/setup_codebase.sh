#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/autogen codebase
git -C codebase checkout 7dd503eccfaafbbe36c427d3cfa29abfa2b3f3f8
# then: bash setup_env.sh && bash run_repro.sh
