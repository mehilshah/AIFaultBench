#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/PythonOT/POT codebase
git -C codebase checkout e330215df11d761582b7942c544166ace69e0151
# then: bash setup_env.sh && bash run_repro.sh
