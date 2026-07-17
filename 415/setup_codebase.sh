#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout ee8dbcb9a53dd42abc7a8ae2ffb9585a24ff3490
# then: bash setup_env.sh && bash run_repro.sh
