#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout b49b8f8d389d6357ab04003a003ef9fa16ee2e43
# then: bash setup_env.sh && bash run_repro.sh
