#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/autogen codebase
git -C codebase checkout 446da624ac091562f4055344b36e6e2115ae5727
# then: bash setup_env.sh && bash run_repro.sh
