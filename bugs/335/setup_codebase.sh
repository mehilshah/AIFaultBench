#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout 62c3e6d8d7b28f6554548e87a5fdc8f05f0fbbb8
# then: bash setup_env.sh && bash run_repro.sh
