#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/patrick-kidger/equinox codebase
git -C codebase checkout d1718838dcfff2b0adc4f7a795f72da7bdbec1aa
# then: bash setup_env.sh && bash run_repro.sh
