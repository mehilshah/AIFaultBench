#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 5aa2d17dd71ab71d129719ba25e261a92f677d80
# then: bash setup_env.sh && bash run_repro.sh
