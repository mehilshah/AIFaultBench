#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/exaloop/codon codebase
git -C codebase checkout dcb41dcfc9438698c8372392160362251f1bd6a3
# then: bash setup_env.sh && bash run_repro.sh
