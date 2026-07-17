#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 05630a7578b25390f469b2f91f2c2326e5ed539b
# then: bash setup_env.sh && bash run_repro.sh
