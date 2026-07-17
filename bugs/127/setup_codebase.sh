#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/exaloop/codon codebase
git -C codebase checkout d13d6a5
# then: bash setup_env.sh && bash run_repro.sh
