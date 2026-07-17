#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/DeepSpeed codebase
git -C codebase checkout df59f203f40c8a292dd019ae68c9e6c88f107026
# then: bash setup_env.sh && bash run_repro.sh
