#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 66921bdde3902dc0acecbc04db4d7c1129da8fcd
# then: bash setup_env.sh && bash run_repro.sh
