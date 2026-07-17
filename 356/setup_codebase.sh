#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout c5fce4e3df4699e3913e0538fe3efffcabbc026b
# then: bash setup_env.sh && bash run_repro.sh
