#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 5b2ccad96a2e8f0567f08714a07aa0baca11c7ef
# then: bash setup_env.sh && bash run_repro.sh
