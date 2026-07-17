#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout ddbd0b876d3cf07d457683d520f00c85f0cc0bb8
# then: bash setup_env.sh && bash run_repro.sh
