#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 1900bc561292177818dfb73946474e79078098ff
# then: bash setup_env.sh && bash run_repro.sh
