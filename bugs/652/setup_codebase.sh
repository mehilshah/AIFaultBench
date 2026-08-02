#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/stanfordnlp/dspy codebase
git -C codebase checkout 8a7bcfd1d345eeefb91b59b177cf7a5c00cd410c
# then: bash setup_env.sh && bash run_repro.sh
