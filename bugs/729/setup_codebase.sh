#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/microsoft/semantic-kernel codebase
git -C codebase checkout cf9a5f21f74782fddfada1d934088fbff6cc24b9
# then: bash setup_env.sh && bash run_repro.sh
