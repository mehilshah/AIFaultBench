#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 0fcf1218c27e7f562cc1f1bae8d9d3c1f9c7d52e
# then: bash setup_env.sh && bash run_repro.sh
