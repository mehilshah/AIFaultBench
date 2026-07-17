#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 0152376a197af90d0ce5198f8375e03069f29f48
# then: bash setup_env.sh && bash run_repro.sh
