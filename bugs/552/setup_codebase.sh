#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 319c515de2a82ac002516ccd4b44dda8e32f7ac4
# then: bash setup_env.sh && bash run_repro.sh
