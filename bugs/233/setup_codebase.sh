#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/equinox codebase
git -C codebase checkout 6a6a441ced2fe64191a087752f1c2e71a6ce39f1
# then: bash setup_env.sh && bash run_repro.sh
