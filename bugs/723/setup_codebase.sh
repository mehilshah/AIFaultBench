#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/modelcontextprotocol/python-sdk codebase
git -C codebase checkout c92bb2f7ffaa61813d7cc350887f4ece38307769
# then: bash setup_env.sh && bash run_repro.sh
