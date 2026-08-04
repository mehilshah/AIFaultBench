#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 17cf5a727f1339f1d9fbf8058b53d2e00e264c4e
# then: bash setup_env.sh && bash run_repro.sh
