#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/camel-ai/camel codebase
git -C codebase checkout adf4aba7f4cf1bf91c247b2b2c51ad11f5374ab2
# then: bash setup_env.sh && bash run_repro.sh
