#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/keras-team/keras-io codebase
git -C codebase checkout f0ec3b083a4ccedc65f371a2aaa9de86df9142bb
# then: bash setup_env.sh && bash run_repro.sh
