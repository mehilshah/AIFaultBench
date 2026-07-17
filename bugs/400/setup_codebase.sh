#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout d49f71825691b554fb8188f8779dc3a5d13e7b96
# then: bash setup_env.sh && bash run_repro.sh
