#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout f87f40ea7c30e2a5e9143a42fd57060680011638
# then: bash setup_env.sh && bash run_repro.sh
