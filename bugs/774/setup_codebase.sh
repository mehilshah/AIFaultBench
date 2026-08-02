#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/browser-use/browser-use codebase
git -C codebase checkout b2641ea3b775aac005736e688a8efef9c88e17b8
# then: bash setup_env.sh && bash run_repro.sh
