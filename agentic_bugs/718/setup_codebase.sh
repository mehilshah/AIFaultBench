#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/browser-use/browser-use codebase
git -C codebase checkout d19ec6ef20e5c68bf4ca198e8b0b5aea69280fe6
# then: bash setup_env.sh && bash run_repro.sh
