#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 6364a19bc97efadd62c9302a56e854e2c90d5edf
# then: bash setup_env.sh && bash run_repro.sh
