#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/python-eel/Eel codebase
git -C codebase checkout ff1fa20d2c3009eb0d5f79000bb998388d9ba086
# then: bash setup_env.sh && bash run_repro.sh
