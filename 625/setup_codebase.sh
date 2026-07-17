#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 7f2f423257592725259a0950094dc9fe9d276a27
# then: bash setup_env.sh && bash run_repro.sh
