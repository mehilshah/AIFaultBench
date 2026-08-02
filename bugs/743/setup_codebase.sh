#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/autogen codebase
git -C codebase checkout 9f2c5aa1be8f59ad830d253294ca84317f859b66
# then: bash setup_env.sh && bash run_repro.sh
