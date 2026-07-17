#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 4e7462990b0e4313ecebdfa8100e51d80925cca1
# then: bash setup_env.sh && bash run_repro.sh
