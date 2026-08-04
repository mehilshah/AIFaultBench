#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/PythonOT/POT codebase
git -C codebase checkout f6139428e70ce964de3bef703ef13aa701a83620
# then: bash setup_env.sh && bash run_repro.sh
