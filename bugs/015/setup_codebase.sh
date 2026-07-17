#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/tensorflow/models codebase
git -C codebase checkout 9a2993d140841f37d73cded94c1295da4faab8b5
# then: bash setup_env.sh && bash run_repro.sh
