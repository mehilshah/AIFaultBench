#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/open-edge-platform/anomalib codebase
git -C codebase checkout c43e552e4178109c1e14ea6aa5f4e2ee03fdca3c
# then: bash setup_env.sh && bash run_repro.sh
