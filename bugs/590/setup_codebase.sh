#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout ab1f0dc6e954ef7d54724386667e33010b2cfc8b
# then: bash setup_env.sh && bash run_repro.sh
