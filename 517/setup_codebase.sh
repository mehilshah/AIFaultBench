#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 611dda1f2e0060af93b329ad1f196788635424b6
# then: bash setup_env.sh && bash run_repro.sh
