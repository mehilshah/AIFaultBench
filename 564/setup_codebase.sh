#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 7c7a7e9a1814adc0ad5e919427723dbab3ee9410
# then: bash setup_env.sh && bash run_repro.sh
