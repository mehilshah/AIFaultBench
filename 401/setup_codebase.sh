#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 0e82cad30f75b892a07e6c9a5f9e24f2cb5d0d81
# then: bash setup_env.sh && bash run_repro.sh
