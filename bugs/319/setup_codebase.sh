#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 2f0924a55de959f88d09451b19b1dac20ac4301a
# then: bash setup_env.sh && bash run_repro.sh
