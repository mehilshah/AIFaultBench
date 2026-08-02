#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/mem0ai/mem0 codebase
git -C codebase checkout e615cc66de7ae8e356d7c37b98200016a32e1d0f
# then: bash setup_env.sh && bash run_repro.sh
