#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 64e71eee1c14dc926d5cbc5e762b6337bb4750a6
# then: bash setup_env.sh && bash run_repro.sh
