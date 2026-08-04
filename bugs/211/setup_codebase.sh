#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/sdv-dev/SDV codebase
git -C codebase checkout f7588077f7c84b87f6f51dc1976adea145ddaf1a
# then: bash setup_env.sh && bash run_repro.sh
