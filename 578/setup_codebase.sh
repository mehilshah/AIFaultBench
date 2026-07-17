#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 43dbb2e67331bd3aa6c73bb5483825432a8b7145
# then: bash setup_env.sh && bash run_repro.sh
