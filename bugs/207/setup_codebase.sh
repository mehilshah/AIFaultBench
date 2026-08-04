#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/PythonOT/POT codebase
git -C codebase checkout 39cd6ec567e94a5edbc47f1bc58a1bd0c58ede3c
# then: bash setup_env.sh && bash run_repro.sh
