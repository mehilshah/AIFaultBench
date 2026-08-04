#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pypa/cibuildwheel codebase
git -C codebase checkout f6c810852d424abdddc6abc44d1e4b165797399d
# then: bash setup_env.sh && bash run_repro.sh
