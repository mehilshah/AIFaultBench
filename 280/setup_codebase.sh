#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/PythonOT/POT codebase
git -C codebase checkout 0411ea22a96f9c22af30156b45c16ef39ffb520d
# then: bash setup_env.sh && bash run_repro.sh
