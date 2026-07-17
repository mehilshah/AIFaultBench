#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout 490a7ff332f65700dd1b43802502f506b8390da3
# then: bash setup_env.sh && bash run_repro.sh
