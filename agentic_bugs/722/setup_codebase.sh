#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/modelcontextprotocol/python-sdk codebase
git -C codebase checkout 3eb579948a4719d606d2adbd1f3f69371c9c0f48
# then: bash setup_env.sh && bash run_repro.sh
