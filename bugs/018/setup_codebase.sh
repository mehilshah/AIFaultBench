#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout efe006c024494e6c513281251213df9af9c62a55
# then: bash setup_env.sh && bash run_repro.sh
