#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout ced727e579c50654bdf264604652d93fe663c0d5
# then: bash setup_env.sh && bash run_repro.sh
