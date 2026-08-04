#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/spulec/freezegun codebase
git -C codebase checkout c8806fa3de2e0280e068deb1761e4452fb5b61f3
# then: bash setup_env.sh && bash run_repro.sh
