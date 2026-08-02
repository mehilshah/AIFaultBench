#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/modelcontextprotocol/python-sdk codebase
git -C codebase checkout b38716e5e3761dd2d52809d2d68ce65325faad5e
# then: bash setup_env.sh && bash run_repro.sh
