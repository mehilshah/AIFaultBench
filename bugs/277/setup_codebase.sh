#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout e708f34b1c0b2c37137196281ba1486be7bebf39
# then: bash setup_env.sh && bash run_repro.sh
