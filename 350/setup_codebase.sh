#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 5f7b687018bd1e0340c661859820fd97aa80a616
# then: bash setup_env.sh && bash run_repro.sh
