#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/semantic-kernel codebase
git -C codebase checkout e73446e86e318f4c437aa7f49ece8c6ba3afba43
# then: bash setup_env.sh && bash run_repro.sh
