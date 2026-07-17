#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 685c7adee65bbcdd6bd6c84c834a0a460f2224eb
# then: bash setup_env.sh && bash run_repro.sh
