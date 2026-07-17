#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/PythonOT/POT codebase
git -C codebase checkout a9bbc2cfdffd22ceee3256102e470df6c25338f3
# then: bash setup_env.sh && bash run_repro.sh
