#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/browser-use/browser-use codebase
git -C codebase checkout ef32ed708ad90b3cffea0b622d54002c0c5fd94a
# then: bash setup_env.sh && bash run_repro.sh
