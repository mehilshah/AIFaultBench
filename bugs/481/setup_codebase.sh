#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 7a3c24ff4b072f3f3df6c0ef9494d1635753c53d
# then: bash setup_env.sh && bash run_repro.sh
