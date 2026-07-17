#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 78c366530db3c26075a63dba370ad002b17b006a
# then: bash setup_env.sh && bash run_repro.sh
