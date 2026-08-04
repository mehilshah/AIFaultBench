#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/equinox codebase
git -C codebase checkout 15a800dd0ab1fc91b033c9305a5fe2f7bf2aecae
# then: bash setup_env.sh && bash run_repro.sh
