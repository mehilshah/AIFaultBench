#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/numpyro codebase
git -C codebase checkout 0d4f40c5a25633591388f12372cdb31f9dff0f29
# then: bash setup_env.sh && bash run_repro.sh
