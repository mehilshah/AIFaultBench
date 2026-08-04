#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout f997da20638fd130c5e581bfff699e05b9b0d033
# then: bash setup_env.sh && bash run_repro.sh
