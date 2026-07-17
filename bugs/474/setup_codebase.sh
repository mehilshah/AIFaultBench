#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 19e32df3a8620d99193d66ccc04ba3e2f1d3a840
# then: bash setup_env.sh && bash run_repro.sh
