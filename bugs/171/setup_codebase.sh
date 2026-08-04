#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/kornia/kornia codebase
git -C codebase checkout bd49f1bee02bc0e2ba04254aed8eaf3a9ccba25c
# then: bash setup_env.sh && bash run_repro.sh
