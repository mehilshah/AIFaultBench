#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/imagen-pytorch codebase
git -C codebase checkout 0d34fe31df013d9c0be072062e224e0df10b1044
# then: bash setup_env.sh && bash run_repro.sh
