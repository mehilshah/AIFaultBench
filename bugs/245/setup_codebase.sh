#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 6a1af1f4795d9b0b179e76ab05a13cc561dcecca
# then: bash setup_env.sh && bash run_repro.sh
