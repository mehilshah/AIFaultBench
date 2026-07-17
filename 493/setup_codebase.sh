#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 8b7e5641228b664b3c9b674a079e95a478f3e2a0
# then: bash setup_env.sh && bash run_repro.sh
