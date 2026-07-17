#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 3b7d7f071c75c75080a910530bb39f0a4ab6479e
# then: bash setup_env.sh && bash run_repro.sh
