#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pytorch/rl codebase
git -C codebase checkout 74abd6c38c065a17aeaa4bd617167055e434fdad
# then: bash setup_env.sh && bash run_repro.sh
